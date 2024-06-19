use std::str::FromStr;
use std::sync::Arc;
use std::sync::Mutex;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyBytes;

use crate::error::IoError;
use crate::fs::FileHandleType;
use crate::fs::SeekFrom;
use crate::fs::{FileHandle, FileSystem};
use crate::terminal::Terminal;

///
/// A small utility function to map an IoError to a PyError.
/// 
fn map_error(error: IoError) -> PyErr {
    PyValueError::new_err(error.to_string())
}

///
/// A small enumeration to determine the whence
/// when seeking in a file.
/// 
#[pyclass]
#[allow(non_camel_case_types)]
pub enum Whence {
    SEEK_SET = 0,
    SEEK_CUR = 1,
    SEEK_END = 2,
}

///
/// A simple wrapper around the FileHandle struct.
/// 
/// This class is a simple wrapper around the FileHandle struct. It defines
/// the basis for a file handle that can be used in Python. The file handle
/// can be used to read and write data to a file.
/// 
/// A file handle is always associated with a filesystem and an inode. The
/// file handle can be used to read and write data to the file.
/// 
#[pyclass]
struct PyFileHandle(Mutex<FileHandle>);

#[pymethods]
impl PyFileHandle {
    ///
    /// Returns a string representation of the file handle.
    /// 
    fn __str__(&self) -> PyResult<String> {
        Ok(format!("{:?}", self.0.lock().unwrap()))
    }

    ///
    /// Returns a string representation of the file handle.
    /// 
    fn id(&self) -> PyResult<u64> {
        self.0.lock().unwrap().id().map_err(map_error)
    }

    ///
    /// Close the file handle.
    /// 
    /// Notice that the pyobject still holds a reference to the file handle. However
    /// any subsequent read or write operation will fail.
    /// 
    /// Small Note on garbage collection: The file handle will internally be closed
    /// HOWEVER it will still keep the file system and inode alive. Until the file
    /// handle is dropped.
    /// 
    fn close(&self) -> PyResult<()> {
        self.0.lock().unwrap().close().map_err(map_error)
    }

    ///
    /// Read data from the file handle.
    /// 
    /// This function reads data from the file handle. The function will return a
    /// byte array with the data that was read from the file. The function will
    /// return an error if the read operation failed.
    /// 
    fn read(&self, py: Python, buffer: usize) -> PyResult<PyObject> {
        let mut buffer = vec![0; buffer];
        let mut handle = self.0.lock().unwrap();
        let result = handle.read(&mut buffer).map_err(map_error)?;
        println!("Read {} bytes from file", result);

        Ok(
            PyBytes::new_bound(py, &buffer[..result])
                .into()
        )
    }

    ///
    /// Write data to the file handle.
    /// 
    /// This function writes data to the file handle. The function will return the
    /// number of bytes that were written to the file. The function will return an
    /// error if the write operation failed.
    /// 
    fn write(&self, buffer: &[u8]) -> PyResult<usize> {
        let mut handle = self.0.lock().unwrap();
        handle.write(buffer).map_err(map_error)
    }

    ///
    /// Seek a certain position in the file.
    /// 
    /// This function seeks a certain position in the file. The function will return
    /// the new position in the file. The function will return an error if the seek
    /// operation failed.
    /// 
    fn seek(&self, offset: usize, whence: &Whence) -> PyResult<()> {
        let whence = match whence {
            Whence::SEEK_SET => SeekFrom::Start(offset),
            Whence::SEEK_CUR => SeekFrom::Current(offset),
            Whence::SEEK_END => SeekFrom::End(offset),
        };

        let mut handle = self.0.lock().unwrap();
        handle.seek(whence).map_err(map_error)
    }

    ///
    /// Tell the current position in the file.
    /// 
    /// This function returns the current position in the file. The function will
    /// return an error if the tell operation failed.
    ///
    fn tell(&self) -> PyResult<usize> {
        let handle = self.0.lock().unwrap();
        handle.tell().map_err(map_error)
    }
}

///
/// An highly simplified binding for a simple filesystem written in Rust.
/// 
/// This class is a simple wrapper around the FileSystem struct. It defines
/// the basis for a small filesystem that can be used in Python. The filesystem
/// can handle files, nested directories and symlinks.
/// 
/// The filesystem is thread-safe and can be shared between multiple threads.
/// 
#[pyclass]
#[derive(Clone)]
struct PyFs(Arc<FileSystem>);

#[pymethods]
impl PyFs {
    ///
    /// Create a new filesystem.
    /// 
    /// This function creates a new filesystem. The filesystem is empty and does
    /// not contain any files or directories. The filesystem is thread-safe and
    /// can be shared between multiple threads.
    /// 
    #[new]
    fn new() -> PyResult<PyFs> {
        Ok(PyFs(Arc::new(FileSystem::new())))
    }

    ///
    /// Returns a string representation of the filesystem.
    /// 
    /// This function returns a string representation of the filesystem. The string
    /// representation contains the number of files and directories in the filesystem.
    /// 
    fn __str__(&self) -> PyResult<String> {
        Ok(format!("{:?}", self.0))
    }

    ///
    /// Create a new directory in the filesystem.
    /// 
    /// This function creates a new directory in the filesystem. The function will
    /// return an error if the directory could not be created.
    /// 
    fn mkdir(&self, path: &str) -> PyResult<()> {
        self.0.mkdir(path).map_err(map_error)
    }

    ///
    /// Create a new file in the filesystem.
    /// 
    /// This function creates a new file in the filesystem. The function will return
    /// an error if the file could not be created.
    /// 
    fn touch(&self, path: &str) -> PyResult<()> {
        self.0.touch(path).map_err(map_error)
    }

    ///
    /// Open a file in the filesystem.
    /// 
    /// This function opens a file in the filesystem. The function will return a file
    /// handle that can be used to read and write data to the file. The function will
    /// return an error if the file could not be opened.
    /// 
    fn open(&self, path: &str, mode: &str) -> PyResult<PyFileHandle> {
        let mode = FileHandleType::from_str(mode)
            .map_err(map_error)?;

        let handle = self.0.clone().open(&path, mode, true).map_err(map_error)?;
        Ok(PyFileHandle(Mutex::new(handle)))
    }

    ///
    /// List the contents of a directory.
    /// 
    /// This function lists the contents of a directory. The function will return a
    /// list of strings with the names of the files and directories in the directory.
    /// The function will return an error if the directory could not be listed.
    ///
    fn listdir(&self, path: &str) -> PyResult<(Vec<String>, Vec<String>)> {
        self.0.ls(&path).map_err(map_error)
    }

    ///
    /// Remove a file from the filesystem.
    /// 
    #[pyo3(text_signature = "(recurse=False)")]
    fn remove(&self, path: &str, recurse: bool) -> PyResult<()> {
        self.0.rm(&path, recurse).map_err(map_error)
    }

    ///
    /// Debug the file system
    /// 
    /// This function will return a debug representation of the filesystem as a string.
    /// 
    fn tree(&self, path: &str, ident: Option<&str>) -> PyResult<String> {
        // First we ls the directory
        let ident = ident.unwrap_or("");
        let (files, dirs) = self.0.ls(&path).map_err(map_error)?;

        // Then we iterate over the files and directories
        let next_ident = format!("{}{}", ident, "  ");

        let mut result = String::new();
        for dir in dirs {
            result.push_str(&format!("{}{}/\n", ident, dir));
            result.push_str(&self.tree(&format!("{}/{}", path, dir), Some(&next_ident))?);
        }

        for file in files {
            result.push_str(&format!("{}{}\n", ident, file));
        }

        Ok(result)
    }
}

///
/// A structure representing a simple terminal
/// 
#[pyclass]
struct PyTerm(Mutex<Terminal>);

#[pymethods]
impl PyTerm {
    ///
    /// Create a new terminal attached to a filesystem.
    /// 
    #[new]
    pub fn new(fs: PyFs) -> PyResult<PyTerm> {
        let fs = fs.0.clone();
        Ok(PyTerm(Mutex::new(Terminal::new(fs))))
    }

    ///
    /// Execute a command in the terminal.
    /// 
    pub fn exec(&self, command: &str) -> PyResult<String> {
        let mut terminal = self.0.lock().unwrap();
        terminal.run(command)
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }
}




#[pymodule]
fn vkernelrs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyFs>()?;
    m.add_class::<PyFileHandle>()?;
    m.add_class::<PyTerm>()?;
    m.add_class::<Whence>()?;

    Ok(())
}
