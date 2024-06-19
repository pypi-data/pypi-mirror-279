use thiserror::Error;

///
/// The error type for the filesystem.
/// 
/// This enum represents the different kinds of errors that can occur in the filesystem.
/// 
#[derive(Debug, Error, PartialEq, Eq)]
pub enum IoError {
    #[error("Inode not found")]
    InodeNotFound,

    #[error("The specified INode is not a directory")]
    NotADirectory,

    #[error("The specified INode is not a file")]
    NotAFile,
    
    #[error("The specified INode is not a symlink")]
    NotASymlink,
    
    #[error("Maximum filesystem depth exceeded")]
    MaxRecursionDepthExceeded,

    #[error("Resource already exists")]
    ResourceAlreadyExists,

    #[error("Directory is not empty")]
    DirectoryIsNotEmpty,
    
    #[error("Resource is currently in use")]
    ResourceCurrentInUse,

    #[error("Unrecognized file mode")]
    UnrecognizedFileMode,


    #[error("File does not support the specified operation: {0}")]
    OperationNotSupported(&'static str),

    #[error("Invalid file descriptor")]
    InvalidFileDescriptor,
}