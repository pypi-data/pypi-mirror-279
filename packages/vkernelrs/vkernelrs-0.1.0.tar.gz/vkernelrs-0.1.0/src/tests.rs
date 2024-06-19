use std::{collections::HashSet, hash::Hash};


fn iters_equal_anyorder<T: Eq + Hash>(mut i1:impl Iterator<Item = T>, i2: impl Iterator<Item = T>) -> bool {
    let set:HashSet<T> = i2.collect();
    i1.all(|x| set.contains(&x))
}

#[cfg(test)]
mod tests {
    use std::sync::Arc;

    use crate::{fs::*, tests::iters_equal_anyorder};

    #[test]
    fn fs_work() {
        let fs = Arc::new(FileSystem::new());
        assert_eq!(fs.mkdir("/test").is_ok(), true);
        assert_eq!(fs.touch("/test/file.txt").is_ok(), true);
        assert_eq!(fs.mkdir("/test/dir").is_ok(), true);
        assert_eq!(fs.touch("/test/dir/file.txt").is_ok(), true);
        assert_eq!(fs.mkdir("/tmp").is_ok(), true);
        assert_eq!(fs.touch("/tmp/file.txt").is_ok(), true);
        assert_eq!(fs.mkdir("/tmp/file.txt").is_err(), true);
        assert_eq!(fs.touch("/tmp").is_err(), true);
        assert_eq!(fs.mkdir("/test").is_err(), true);
        assert_eq!(fs.touch("/test/dir").is_err(), true);
    }

    #[test]
    fn fs_file_work() {
        let fs = Arc::new(FileSystem::new());
        
        // Create a file
        let f = fs.clone().open(&"/test.txt", FileHandleType::WRITE, true);
        assert_eq!(f.is_ok(), true);
        let mut f = f.unwrap();

        let data = b"Hello, World!";
        assert_eq!(f.write(data).is_ok(), true);
        assert_eq!(f.close().is_ok(), true);

        // Read the file
        let f = fs.open(&"/test.txt", FileHandleType::READ, true);
        assert_eq!(f.is_ok(), true);
        let mut f = f.unwrap();
        
        let mut buffer = vec![0; 512];
        let resp = f.read(&mut buffer);
        assert_eq!(resp.is_ok(), true);
        let read_data = &buffer[0..resp.unwrap()];

        assert_eq!(read_data, data);
    }

    #[test]
    fn fs_basic_remove_work() {
        let fs = Arc::new(FileSystem::new());

        // Create a file
        assert_eq!(fs.touch("/test").is_ok(), true);

        // Remove the file
        assert_eq!(fs.rm("/test", false).is_ok(), true);

        // Create a directory
        assert_eq!(fs.mkdir("/test").is_ok(), true);

        // Remove the directory
        assert_eq!(fs.rm("/test", false).is_ok(), true);

        // Fail to find the directory
        assert_eq!(fs.mkdir("/test/dir").is_err(), true);
    }

    #[test]
    fn fs_recursive_remove_work() {
        let fs = Arc::new(FileSystem::new());

        // Create a directory
        assert_eq!(fs.mkdir("/test").is_ok(), true);
        assert_eq!(fs.mkdir("/test/dir").is_ok(), true);

        // Create a file
        assert_eq!(fs.touch("/test/dir/file.txt").is_ok(), true);

        // Remove the directory
        assert_eq!(fs.rm("/test", true).is_ok(), true);

        // Fail to find the directory
        assert_eq!(fs.mkdir("/test/dir").is_err(), true);
    }

    #[test]
    fn path_display_work() {
        let fs = Arc::new(FileSystem::new());

        // Create a directory
        assert_eq!(fs.mkdir("/test").is_ok(), true);
        assert_eq!(fs.mkdir("/test/dir").is_ok(), true);

        // Create a file
        assert_eq!(fs.touch("/test/dir/file.txt").is_ok(), true);

        // Retrieve the NodeId of the file
        let node_id = fs.get_inode_by_path_raw(&"/test/dir/file.txt");
        assert_eq!(node_id.is_ok(), true);
        let node_id = node_id.unwrap();

        // Retrieve the path of the file
        assert_eq!(fs.get_path_by_inode(node_id), Ok("/test/dir/file.txt".to_string()));
    }

    #[test]
    fn path_listing_work() {
        let fs = Arc::new(FileSystem::new());

        // Create a directory
        assert_eq!(fs.mkdir("/tmp").is_ok(), true);
        assert_eq!(fs.mkdir("/tmp/dir").is_ok(), true);
        assert_eq!(fs.touch("/tmp/file.txt").is_ok(), true);
        assert_eq!(fs.touch("/tmp/dir/file.txt").is_ok(), true);
        assert_eq!(fs.touch("/tmp/41.txt").is_ok(), true);

        // List the directory
        let listing = fs.ls(&"/tmp");
        assert_eq!(listing.is_ok(), true);
        let listing = listing.unwrap();
        let (files, dirs) = listing;

        assert_eq!(iters_equal_anyorder(files.iter(), vec!["41.txt".to_string(), "file.txt".to_string()].iter()), true);
        assert_eq!(iters_equal_anyorder(dirs.iter(), vec!["dir".to_string()].iter()), true);
    }

    #[test]
    fn is_file_and_is_dir_work() {
        let fs = Arc::new(FileSystem::new());

        // Create some files
        assert_eq!(fs.touch("/file.txt").is_ok(), true);
        assert_eq!(fs.mkdir("/dir").is_ok(), true);

        // Retrieve the inode of both files and dirs
        assert_eq!(fs.is_file(&"/file.txt"), Ok(true));
        assert_eq!(fs.is_directory(&"/file.txt"), Ok(false));
        assert_eq!(fs.is_file(&"/dir"), Ok(false));
        assert_eq!(fs.is_directory(&"/dir"), Ok(true));
    }
}