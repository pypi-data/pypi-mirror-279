use std::{str::FromStr, sync::{atomic::{AtomicIsize, AtomicU64, Ordering}, Arc, RwLock}};

use chashmap::{CHashMap, ReadGuard};
use compact_str::CompactString;
use smallvec::SmallVec;
use bitflags::bitflags;

use crate::error::IoError;

///
/// The type of an inode id.
/// 
pub type INodeId = u64;
pub type AtomicNodeId = AtomicU64;

bitflags! {
    ///
    /// This enum represents the different kinds of file handle types.
    /// 
    /// A file handle can be read-only, write-only, or both.
    /// 
    /// The read flag allows reading from the file.
    /// The write flag allows writing to the file.
    /// 
    #[derive(Default, Debug, Clone, Copy, PartialEq, Eq)]
    pub struct FileHandleType: u32 {
        const EMPTY = 0;

        const READ = 1 << 0;
        const WRITE = 1 << 1;
    }
}

impl FromStr for FileHandleType {
    type Err = IoError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut result = FileHandleType::EMPTY;

        for c in s.chars() {
            match c {
                'r' if !result.contains(FileHandleType::READ) => result |= FileHandleType::READ,
                'w' if !result.contains(FileHandleType::WRITE) => result |= FileHandleType::WRITE,
                _ => return Err(IoError::UnrecognizedFileMode)
            }
        }

        Ok(result)
    }
}

///
/// Seek operation for file handle
/// 
pub enum SeekFrom {
    Start(usize),
    End(usize),
    Current(usize),
}

///
/// A structure that represents the content of a file as stored in the file system.
/// 
#[derive(Debug)]
pub struct FileData {
    pub data: SmallVec<[u8; 32]>,
}

impl Default for FileData {
    fn default() -> Self {
        Self {
            data: SmallVec::new(),
        }
    }
}

///
/// This enum represents the different kinds of inodes that can be stored in the filesystem.
/// Namely, a file inode, a directory inode, or a symlink inode.
/// 
/// The file inode contains the data of the file.
/// The directory inode contains a list of the children inodes.
/// The symlink inode contains the path to the target.
/// 
/// The data field is a CompactString, which is a string that is stored in a compact form.
/// This is useful for storing strings in a more memory-efficient way.
/// 
#[derive(Debug)]
pub enum INodeKind {
    File {
        data: FileData,
        lock: FileLock
    },
    Directory {
        children: SmallVec<[INodeId; 8]>
    },
    Symlink {
        target: INodeId
    }
}

///
/// This struct represents a lock on an inode. Lock can occur in two ways: shared or exclusive.
/// 
/// A shared lock allows multiple readers to access the inode at the same time.
/// An exclusive lock allows only one writer to access the inode at a time.
/// 
#[derive(Debug)]
pub struct FileLock {
    flag: AtomicIsize
}

impl FileLock {
    /// 
    /// Acquire write only for files (not directory)
    /// 
    const WRITE_EXCLUSIVE: isize = -1;
    const LOCK_EXCLUSIVE: isize = -2;

    pub fn new() -> Self {
        FileLock {
            flag: AtomicIsize::new(0),
        }
    }

    fn try_acquire_read(&self) -> bool {
        let mut flag = self.flag.load(Ordering::Acquire);

        loop {
            if flag < 0 {
                return false;
            }

            match self.flag.compare_exchange_weak(flag, flag + 1, Ordering::AcqRel, Ordering::Acquire) {
                Ok(_) => return true,
                Err(x) => flag = x,
            }
        }
    }

    fn try_acquire_write(&self) -> bool {
        let mut flag = self.flag.load(Ordering::Acquire);

        loop {
            if flag != 0 {
                return false;
            }

            match self.flag.compare_exchange_weak(flag, FileLock::WRITE_EXCLUSIVE, Ordering::AcqRel, Ordering::Acquire) {
                Ok(_) => return true,
                Err(x) => flag = x,
            }
        }
    }

    fn try_acquire_exclusive(&self) -> bool {
        let mut flag = self.flag.load(Ordering::Acquire);

        loop {
            if flag != 0 {
                return false;
            }

            match self.flag.compare_exchange_weak(flag, FileLock::LOCK_EXCLUSIVE, Ordering::AcqRel, Ordering::Acquire) {
                Ok(_) => return true,
                Err(x) => flag = x,
            }
        }
    }

    fn release_write(&self) {
        assert!(self.flag.load(Ordering::Acquire) == FileLock::WRITE_EXCLUSIVE);
        self.flag.store(0, Ordering::Release);
    }

    // fn release_exclusive(&self) {
    //     assert!(self.flag.load(Ordering::Acquire) == FileLock::LOCK_EXCLUSIVE);
    //     self.flag.store(0, Ordering::Release);
    // }

    fn release_read(&self) {
        let mut flag = self.flag.load(Ordering::Acquire);

        loop {
            assert!(flag > 0);

            match self.flag.compare_exchange_weak(flag, flag - 1, Ordering::AcqRel, Ordering::Acquire) {
                Ok(_) => return,
                Err(x) => flag = x,
            }
        }
    }
}


///
/// Define a file handle struct that represents a handle to a file in the filesystem.
/// 
/// The file handle contains an id, a type, and a reference to the filesystem.
/// 
/// The id is a unique identifier for the file handle.
/// The type is the type of the file handle (read, write, or both).
/// The fs is a reference to the filesystem.
/// 
#[derive(Debug)]
pub struct FileHandle {
    id: Option<INodeId>,
    r#type: FileHandleType,
    fs: Arc<FileSystem>,
    offset: usize,
}

impl FileHandle {
    ///
    /// Create a new file handle with the given filesystem, id, and type.
    /// 
    /// The file handle is created by locking the corresponding inode.
    /// 
    fn new(fs: Arc<FileSystem>, id: INodeId, r#type: FileHandleType) -> Result<Self, IoError> {
        // retrieve the inode corresponding to the file handle
        let inode = fs.get_inode(id)?;
        
        // lock the corresponding inode (either shared or exclusive)
        match &*inode.data.read().unwrap() {
            INodeKind::File { lock, .. } => {
                let success = if r#type.contains(FileHandleType::WRITE) {
                    lock.try_acquire_write()
                }
                else {
                    lock.try_acquire_read()
                };

                if !success {
                    return Err(IoError::ResourceCurrentInUse);
                }
            },
            _ => return Err(IoError::NotAFile)
        };
        drop(inode);

        // create the file handle
        Ok(Self {
            id: Some(id),
            r#type,
            fs,
            offset: 0
        })
    }

    ///
    /// Return the file handle id (inode id).
    /// 
    /// The id is a unique identifier for the file handle.
    /// 
    pub fn id(&self) -> Result<INodeId, IoError> {
        self.id.ok_or(IoError::InvalidFileDescriptor)
    }

    ///
    /// Read data from the file handle into the buffer.
    /// 
    /// The read operation is performed by reading the data from the file.
    /// 
    /// The read operation is supported only if the file handle type contains the read flag.
    /// 
    pub fn read(&mut self, buffer: &mut[u8]) -> Result<usize, IoError> {
        let id = self.id.ok_or(IoError::InvalidFileDescriptor)?;

        // Check if read operation is supported
        if !self.r#type.contains(FileHandleType::READ) {
            return Err(IoError::OperationNotSupported("read"));
        }

        // Retrieve the inode corresponding to the file handle
        let inode = self.fs.get_inode(id)?;

        let guard = inode.data.read().unwrap();
        let data = match &*guard {
            INodeKind::File { data, .. } => &data.data,
            _ => return Err(IoError::NotAFile)
        };


        // Retrieve the data from the file
        let len = buffer.len().min(data.len() - self.offset);

        // Perform the read operation
        buffer[..len].copy_from_slice(&data[self.offset..self.offset + len]);
        self.offset += len;
        Ok(len)
    }

    ///
    /// Write data from the buffer into the file handle.
    /// 
    /// The write operation is performed by writing the data to the file.
    /// 
    /// The write operation is supported only if the file handle type contains the write flag.
    /// 
    pub fn write(&mut self, buffer: &[u8]) -> Result<usize, IoError> {
        let id = self.id.ok_or(IoError::InvalidFileDescriptor)?;

        // Check if write operation is supported
        if !self.r#type.contains(FileHandleType::WRITE) {
            return Err(IoError::OperationNotSupported("write"));
        }

        // Retrieve the inode corresponding to the file handle
        return match &mut *self.fs.get_inode(id)?.data.write().unwrap() {
            INodeKind::File { data, .. } => {
                // Check if we need to resize the data buffer
                if self.offset + buffer.len() > data.data.len() {
                    data.data.resize(self.offset + buffer.len(), 0);
                }

                // Perform the write operation
                data.data[self.offset..self.offset + buffer.len()].copy_from_slice(buffer);
                Ok(buffer.len())
            }
            _ => Err(IoError::NotAFile)
        };
    }

    ///
    /// Seek to a specific offset in the file handle.
    /// 
    /// The seek operation is performed by setting the offset of the file handle.
    /// 
    pub fn tell(&self) -> Result<usize, IoError> {
        if self.id.is_none() {
            return Err(IoError::InvalidFileDescriptor);
        }

        Ok(self.offset)
    }

    ///
    /// Seek to a specific offset in the file handle.
    /// 
    pub fn seek(&mut self, data: SeekFrom) -> Result<(), IoError> {
        let id = self.id.ok_or(IoError::InvalidFileDescriptor)?;

        // Determine the size of the file
        let inode = self.fs.get_inode(id)?;
        let guard = inode.data.read().unwrap();
        let size = match &*guard {
            INodeKind::File { data, .. } => data.data.len(),
            _ => return Err(IoError::NotAFile)
        };

        // Perform the seek operation
        self.offset = match data {
            SeekFrom::Start(offset) => offset.min(size),
            SeekFrom::End(offset) => size.saturating_sub(offset),
            SeekFrom::Current(offset) => self.offset.saturating_add(offset),
        }.min(size);

        Ok(())
    }

    ///
    /// Close the file handle.
    /// 
    pub fn close(&mut self) -> Result<(), IoError> {
        let id = self.id.ok_or(IoError::InvalidFileDescriptor)?;

        // Release the lock on the inode
        let inode = self.fs.get_inode(id)?;
        match &*inode.data.read().unwrap() {
            INodeKind::File { lock, .. } => {
                if self.r#type.contains(FileHandleType::WRITE) {
                    lock.release_write();
                }
                else {
                    lock.release_read();
                }
            },
            _ => return Err(IoError::NotAFile)
        };

        self.id = None;
        Ok(())
    }
}

impl Drop for FileHandle {
    fn drop(&mut self) {
        if self.id.is_some() {
            self.close().unwrap();
        }
    }
}


///
/// Implementation of the INode struct. This struct represents an inode in the filesystem.
/// 
/// An inode has an id, a parent id, a lock, a name, and data.
/// 
/// The id is a unique identifier for the inode.
/// The parent id is the id of the parent inode.
/// The lock is a lock on the inode.
/// 
#[derive(Debug)]
pub struct INode {
    id: INodeId,
    parent: INodeId,
    depth: usize,
    name: CompactString,
    data: RwLock<INodeKind>,
}

///
/// Implementation of the FileSystem struct. This struct represents the filesystem.
/// 
/// The filesystem contains a list of inodes and a list of free inodes.
/// 
#[derive(Debug)]
pub struct FileSystem {
    inodes: CHashMap<INodeId, INode>,
    next_inode_id: AtomicNodeId,
}

impl FileSystem {
    const ROOT_INODE_ID: INodeId = 0;
    const MAX_FS_DEPTH: usize = 64;

    ///
    /// This function creates a new inode in the filesystem.
    /// 
    fn create_inode_id(&self) -> INodeId {
        self.next_inode_id.fetch_add(1, Ordering::Relaxed)
    }

    ///
    /// This function deletes an inode from the filesystem.
    /// 
    fn release_inode_id(&self, id: INodeId) {
        self.inodes.remove(&id);
    }

    ///
    /// Resolve the inode by following symlinks.
    /// 
    fn get_inode_raw(&self, id: INodeId) -> Result<INodeId, IoError> {
        self.inodes.get(&id)
            .ok_or(IoError::InodeNotFound)
            .and_then(|inode| {
                match *inode.data.read().unwrap() {
                    INodeKind::Symlink { target } => self.get_inode_raw(target),
                    _ => Ok(id)
                }
            })
    }

    ///
    /// Validate the name of a file or directory.
    /// 
    fn validate_name(name: &str) -> Result<(), IoError> {
        if name.is_empty() {
            return Err(IoError::ResourceAlreadyExists);
        }

        if name.contains(&['/', '\\']) {
            return Err(IoError::ResourceAlreadyExists);
        }

        if name == "." || name == ".." {
            return Err(IoError::ResourceAlreadyExists);
        }

        Ok(())
    }

    ///
    /// Resolve the inode by following symlinks.
    /// 
    fn get_inode(&self, id: INodeId) -> Result<ReadGuard<'_, INodeId, INode>, IoError> {
        self.get_inode_raw(id)
            .and_then(|id| self.inodes.get(&id).ok_or(IoError::InodeNotFound))
    }

    ///
    /// Find a inode by name in a directory inode.
    /// 
    fn find_inode_by_name_with_handle(&self, parent_inode: &INode, name: &str, include_meta: bool) -> Result<INodeId, IoError> {
        if include_meta {
            if name == "." || name == "" {
                return Ok(parent_inode.id);
            }
            else if name == ".." {
                return Ok(parent_inode.parent);
            }
        }

        return match &*parent_inode.data.read().unwrap() {
            INodeKind::Directory { children } => {
                for child in children.iter() {
                    let child_inode = self.get_inode(*child)?;
                    if child_inode.name == name {
                        return Ok(*child);
                    }
                }

                return Err(IoError::InodeNotFound)
            }
            _ => Err(IoError::NotADirectory)
        };
    }

    pub fn find_inode_by_name(&self, parent: INodeId, name: &str) -> Result<INodeId, IoError> {
        let parent_inode = self.get_inode(parent)?;
        self.find_inode_by_name_with_handle(&parent_inode, name, true)
    }

    pub fn is_file_raw(&self, id: INodeId) -> Result<bool, IoError> {
        let inode = self.get_inode(id)?;
        let is_file = match &*inode.data.read().unwrap() {
            INodeKind::File { .. } | INodeKind::Symlink { .. } => true,
            _ => false
        };
        return Ok(is_file);
    }

    pub fn is_file<P: AsRef<str>>(&self, path: &P) -> Result<bool, IoError> {
        self.is_file_raw(self.get_inode_by_path_raw(path)?)
    }

    pub fn is_directory_raw(&self, id: INodeId) -> Result<bool, IoError> {
        let inode = self.get_inode(id)?;
        let is_directory = match &*inode.data.read().unwrap() {
            INodeKind::Directory { .. } => true,
            _ => false
        };
        return Ok(is_directory);
    }

    pub fn is_directory<P: AsRef<str>>(&self, path: &P) -> Result<bool, IoError> {
        self.is_directory_raw(self.get_inode_by_path_raw(path)?)
    }

    ///
    /// Retrieve a inode by its path
    /// 
    fn get_inode_by_path<P: AsRef<str>>(&self, path: &P) -> Result<ReadGuard<'_, INodeId, INode>, IoError> {
        let mut current_inode = self.get_inode(FileSystem::ROOT_INODE_ID)?;

        for part in path.as_ref().split(&['/', '\\']) {
            if part.is_empty() || part == "." {
                continue;
            }

            if part == ".." {
                current_inode = self.get_inode(current_inode.parent)?;
                continue;
            }

            let inode_id = self.find_inode_by_name_with_handle(&*current_inode, part, true)?;
            current_inode = self.get_inode(inode_id)?;
        }

        Ok(current_inode)
    }

    pub fn get_inode_by_path_raw<P: AsRef<str>>(&self, path: &P) -> Result<INodeId, IoError> {
        self.get_inode_by_path(path).map(|x| x.id)
    }

    ///
    /// Get the path of a inode by its inode id.
    /// 
    /// This function returns the path of the inode as a string.
    /// 
    pub fn get_path_by_inode(&self, mut inode: INodeId) -> Result<String, IoError> {
        let mut path_fragment: SmallVec<[CompactString; 8]> = SmallVec::new();

        loop {
            if inode == FileSystem::ROOT_INODE_ID {
                break;
            }

            let new_inode = self.get_inode(inode)?;
            inode = new_inode.parent;
            path_fragment.push(new_inode.name.clone());
        }

        let string = path_fragment.iter().rev().map(|x| x.to_string()).collect::<Vec<String>>().join("/");
        Ok(format!("/{}", string))
    }

    ///
    /// Create a new INode with the given parent, name, and data.
    /// 
    fn create_inode(&self, parent: INodeId, name: CompactString, data: INodeKind) -> Result<INodeId, IoError> {
        // Validate the name of the inode
        Self::validate_name(&name)?;

        // Retrieve a new inode id
        let id = self.create_inode_id();

        // Find the parent inode
        let parent_inode = self.get_inode(parent)?;

        // Check that no inode with the same name already exists
        if let Ok(_) = self.find_inode_by_name_with_handle(&parent_inode, &name, true) {
            return Err(IoError::ResourceAlreadyExists);
        }

        // Create the inode
        let inode = INode {
            id,
            parent,
            depth: parent_inode.depth + 1,
            name,
            data: RwLock::new(data),
        };
        if inode.depth > FileSystem::MAX_FS_DEPTH {
            return Err(IoError::MaxRecursionDepthExceeded);
        }

        // Create the new inode
        match &mut *parent_inode.data.write().unwrap() {
            INodeKind::Directory { children } => {
                children.push(id);
                Ok(())
            }
            _ => Err(IoError::NotADirectory)
        }?;

        // Insert the new inode into the filesystem
        self.inodes.insert(id, inode);
        Ok(id)
    }

    ///
    /// A small function utility to remove an inode from a directory.
    /// 
    fn remove_inode(&self, id: INodeId, data_callback: impl FnOnce(&INodeKind) -> Result<(), IoError>) -> Result<(), IoError> {
        let inode = self.get_inode(id)?;
        let parent_inode = self.get_inode(inode.parent)?;
        
        // Check whether we can safely remove the inode
        data_callback(&*inode.data.read().unwrap())?;

        // Remove the inode from the parent directory
        match &mut *parent_inode.data.write().unwrap() {
            INodeKind::Directory { children } => {
                children.retain(|x| *x != id);
                Ok(())
            }
            _ => Err(IoError::NotADirectory)
        }?;

        // We need to release the inode guard before we can remove the inode
        // otherwise we will have a deadlock
        drop(inode);

        self.release_inode_id(id);
        Ok(())
    }

    ///
    /// This function creates a new filesystem with a root inode.
    /// 
    pub fn new() -> FileSystem {
        let lock = FileLock::new();
        lock.try_acquire_read(); // Lock is acquired by default for the root inode (so that it cannot be deleted)

        let inodes = CHashMap::new();
        inodes.insert(
            FileSystem::ROOT_INODE_ID,
            INode {
                id: FileSystem::ROOT_INODE_ID,
                parent: FileSystem::ROOT_INODE_ID,
                depth: 0,
                name: CompactString::from(""),
                data: RwLock::new(
                    INodeKind::Directory {
                        children: SmallVec::new()
                    }
                )
            }
        );

        FileSystem {
            inodes,
            next_inode_id: AtomicNodeId::new(1),
        }
    }

    ///
    /// Create a new directory into the filesystem with the given name.
    /// 
    pub fn create_directory<P: AsRef<str>>(&self, parent: INodeId, name: P) -> Result<INodeId, IoError> {
        self.create_inode(
            parent,
            CompactString::from(name.as_ref()),
            INodeKind::Directory {
                children: SmallVec::new()
            }
        )
    }

    pub fn mkdir_raw(&self, parent: INodeId, name: &str) -> Result<INodeId, IoError> {
        self.create_directory(parent, name)
    }

    pub fn mkdir<P: AsRef<str>>(&self, path: P) -> Result<(), IoError> {
        let (parent_path, name) = path.as_ref().rsplit_once(&['/', '\\'])
            .unwrap_or(("", path.as_ref()));

        let parent = self.get_inode_by_path_raw(&parent_path)?;
        self.create_directory(parent, name)
            .map(|_| ())
    }

    ///
    /// Create a new file into the filesystem with the given name and data.
    /// 
    pub fn create_file<P: AsRef<str>>(&self, parent: INodeId, name: P) -> Result<INodeId, IoError> {
        let lock = FileLock::new();

        self.create_inode(
            parent,
            CompactString::from(name.as_ref()),
            INodeKind::File {
                data: FileData::default(),
                lock
            }
        )
    }

    pub fn touch_raw(&self, parent: INodeId, name: &str) -> Result<INodeId, IoError> {
        self.create_file(parent, name)
    }

    pub fn touch<P: AsRef<str>>(&self, path: P) -> Result<(), IoError> {
        let (parent_path, name) = path.as_ref().rsplit_once(&['/', '\\'])
            .unwrap_or(("", path.as_ref()));

        let parent = self.get_inode_by_path_raw(&parent_path)?;

        self.create_file(parent, name)
            .map(|_| ())
    }

    ///
    /// Remove a file (or symlink) from the filesystem.
    /// 
    pub fn remove_file(&self, id: INodeId) -> Result<(), IoError> {
        self.remove_inode(id, |data| {
            match data {
                INodeKind::File { lock, .. } => {
                    if lock.try_acquire_exclusive() {
                        Ok(())
                    }
                    else {
                        Err(IoError::ResourceCurrentInUse)
                    }
                }
                INodeKind::Symlink { .. } => Ok(()),
                _ => Err(IoError::NotAFile)
            }
        })
    }

    ///
    /// Remove a directory from the filesystem.
    /// 
    pub fn remove_directory(&self, id: INodeId) -> Result<(), IoError> {
        self.remove_inode(id, |data| {
            match data {
                INodeKind::Directory { children } => {
                    if children.is_empty() {
                        Ok(())
                    }
                    else {
                        Err(IoError::DirectoryIsNotEmpty)
                    }
                }
                _ => Err(IoError::NotADirectory)
            }
        })
    }

    ///
    /// Remove a file or directory from the filesystem with a raw inode id.
    /// 
    /// The recurse flag determines whether to remove the file or directory recursively.
    /// 
    /// If recurse is true, the function will remove the file or directory and all its children.
    /// If recurse is false, the function will remove the file or directory only if it is empty.
    /// 
    fn rm_raw(&self, inode: INodeId, recurse: bool) -> Result<(), IoError> {
        
        // Check if the inode is a file or a directory
        let mut all_children: Option<SmallVec<[INodeId; 8]>> = None;

        let is_file = match &*self.get_inode(inode)?.data.read().unwrap() {
            INodeKind::File { .. } | INodeKind::Symlink { .. } => {
                true
            }
            INodeKind::Directory { children } => {
                if recurse {
                    all_children = Some(children.iter().cloned().collect());
                }
                else if children.len() > 0 {
                    return Err(IoError::DirectoryIsNotEmpty);
                }
                false
            }
        };

        // Remove the children of the directory
        if let Some(children) = all_children {
            for child in children {
                self.rm_raw(child, true)?;
            }
        }

        // We need to delay the removal of the inode until we have 
        // release the read lock on the inode otherwise we will have a deadlock
        if is_file {
            self.remove_file(inode)?;
        }
        else {
            self.remove_directory(inode)?;
        }

        Ok(())
    }

    ///
    /// Remove a file or directory from the filesystem.
    /// 
    /// The recurse flag determines whether to remove the file or directory recursively.
    /// 
    /// If recurse is true, the function will remove the file or directory and all its children.
    /// If recurse is false, the function will remove the file or directory only if it is empty.
    /// 
    pub fn rm<P: AsRef<str>>(&self, path: P, recurse: bool) -> Result<(), IoError> {
        let inode = self.get_inode_by_path_raw(&path)?;
        self.rm_raw(inode, recurse)
    }

    ///
    /// List all the children of a directory.
    /// 
    pub fn list_directory(&self, id: INodeId) -> Result<Vec<INodeId>, IoError> {
        let inode = self.get_inode(id)?;
        return match &*inode.data.read().unwrap() {
            INodeKind::Directory { children } => {
                Ok(children.iter().cloned().collect())
            }
            _ => Err(IoError::NotADirectory)
        };
    }

    pub fn ls_raw(&self, inode: INodeId) -> Result<(Vec<String>, Vec<String>), IoError> {
        let mut files: Vec<String> = Vec::new();
        let mut dirs: Vec<String> = Vec::new();

        self.list_directory(inode)?
            .into_iter()
            .for_each(|x| {
                let inode = self.get_inode(x).unwrap();
                
                return match &*inode.data.read().unwrap() {
                    INodeKind::File { .. } | INodeKind::Symlink { .. } => {
                        files.push(inode.name.to_string());
                    }
                    INodeKind::Directory { .. } => {
                        dirs.push(inode.name.to_string());
                    }
                };
            });

        Ok((files, dirs))
    }

    pub fn ls<P: AsRef<str>>(&self, path: &P) -> Result<(Vec<String>, Vec<String>), IoError> {
        self.ls_raw(self.get_inode_by_path_raw(path)?)
    }

    ///
    /// Open a filehandle to a file.
    /// 
    pub fn open_raw(self: Arc<Self>, inode: INodeId, handle_type: FileHandleType) -> Result<FileHandle, IoError> {
        // Attempt to find the inode by name
        let inode = self.get_inode_raw(inode)?;
        if !self.is_file_raw(inode)? {
            return Err(IoError::NotAFile);
        }

        // Create the file handle
        FileHandle::new(self, inode, handle_type)
    }

    pub fn open<P: AsRef<str>>(self: Arc<Self>, path: &P, handle_type: FileHandleType, create: bool) -> Result<FileHandle, IoError> {
        // Split the path between parent and name
        let (parent_path, name) = path.as_ref().rsplit_once(&['/', '\\'])
            .unwrap_or(("", path.as_ref()));

        // Find the parent inode
        let parent = self.get_inode_by_path_raw(&parent_path)?;
        
        // Attempt to find the inode by name
        let id = self.find_inode_by_name(parent, name);
        let id = if id.is_err() && create {
            let err = id.unwrap_err();
            if err == IoError::InodeNotFound {
                self.create_file(parent, name)?
            }
            else {
                return Err(err);
            }
        }
        else {
            id?
        };

        // Create the file handle
        FileHandle::new(self, id, handle_type)
    }
}

