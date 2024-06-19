use std::{collections::HashMap, sync::Arc};

use lazy_static::lazy_static;

use crate::fs::{FileHandleType, FileSystem, INodeId, SeekFrom};

///
/// A type alias for any function that can be run in the terminal
/// 
/// The function takes in the terminal context and the arguments
/// and returns a result
/// 
type Command = &'static (dyn Fn(&mut TerminalContext, &[String]) -> Result<String, String> + Sync + Send);

lazy_static! {
    ///
    /// A list of commands that the terminal can run
    /// 
    static ref COMMANDS: HashMap<&'static str, Command> = {
        let mut map = HashMap::new();
        map.insert("cd", &cmd_cd as Command);
        map.insert("ls", &cmd_ls as Command);
        map.insert("pwd", &cmd_pwd as Command);
        map.insert("cat", &cmd_cat as Command);
        map.insert("mkdir", &cmd_mkdir as Command);
        map.insert("touch", &cmd_touch as Command);
        map.insert("help", &cmd_help as Command);
        map
    };
}

///
/// The context of the terminal
/// 
/// This is used to store the state of the terminal
/// 
pub struct TerminalContext {
    current_dir: INodeId,
    fs: Arc<FileSystem>,
}

impl TerminalContext {
    ///
    /// Retrieve the target INodeId based on a path
    /// 
    fn get_target_inode(&self, mut path: &str) -> Result<INodeId, String> {
        let root_dir: INodeId = if path.starts_with("/") {
            path = &path[1..]; // Skip the first '/'
            0
        } else {
            self.current_dir
        };

        // Find the node id of the path
        self.fs.find_inode_by_name(root_dir, path)
            .map_err(|e| format!("{}: {}", path, e))
    }
}

///
/// A *very* simple terminal emulator
/// 
/// Notice that we will probably move away from this design in the future
/// due to the complexity of terminal emulators
/// 
pub struct Terminal {
    context: TerminalContext,
}

///
/// Implement the terminal
/// 
impl Terminal {
    ///
    /// Create a new terminal
    /// 
    pub fn new(fs: Arc<FileSystem>) -> Terminal {
        Terminal {
            context: TerminalContext {
                current_dir: 0, // The terminal starts at the root directory
                fs,
            }
        }
    }
    
    ///
    /// Run a command in the terminal
    /// 
    pub fn run(&mut self, command: &str) -> Result<String, String> {
        // Split the command into parts
        let value = shlex::split(command);
        if value.is_none() {
            return Err("The command was not correctly formatted".to_string());
        }
        let value = value.unwrap();
        if value.is_empty() {
            return Ok("".to_string());
        }

        // Get the command and the arguments
        let (command, args) = value.split_first().unwrap();
        let command = &*command;

        // Get the command
        let command_fn = COMMANDS.get(command.as_str());
        if command_fn.is_none() {
            return Err(format!("{}: command not found", command));
        }

        // Run the command
        return command_fn.unwrap()(&mut self.context, args);
    }
}

///
/// Chande the current directory
/// 
fn cmd_cd(context: &mut TerminalContext, args: &[String]) -> Result<String, String> {
    if args.len() < 1 {
        return Err("cd: missing argument".to_string());
    }

    // Retrieve the root directory
    let path = &args[0];
    let node_id = context.get_target_inode(path)
        .map_err(|e| format!("cd: cannot access '{}': {}", path, e))?;
    
    if !context.fs.is_directory_raw(node_id)
        .map_err(|e| format!("cd: cannot access '{}': {}", path, e))?
    {
        return Err(format!("cd: {}: Not a directory", path));
    }

    // Change the current directory
    context.current_dir = node_id;
    Ok("".to_string())
}

///
/// List the contents of the current directory
/// 
fn cmd_ls(context: &mut TerminalContext, args: &[String]) -> Result<String, String> {
    // Retrieve the target directory
    let target_dir: INodeId = if args.len() < 1 {
        context.current_dir
    } else {
        context.get_target_inode(&args[0])?
    };

    // Ensure that the target directory is a directory
    if !context.fs.is_directory_raw(target_dir)
        .map_err(|e| format!("ls: cannot access '{}': {}", target_dir, e))?
    {
        return Err(format!("ls: {}: Not a directory", target_dir));
    }

    // List all file and directories within the target directory
    let (files, dirs) = context.fs.ls_raw(target_dir)
        .map_err(|e| format!("ls: cannot access '{}': {}", target_dir, e))?;

    // Format the output
    let mut result = String::new();
    for file in files {
        result.push_str(&format!("{}\n", file));
    }
    for dir in dirs {
        result.push_str(&format!("{}/\n", dir));
    }

    Ok(result)
}

///
/// Print the current working directory
/// 
fn cmd_pwd(context: &mut TerminalContext, _args: &[String]) -> Result<String, String> {
    context.fs.get_path_by_inode(context.current_dir)
        .map_err(|e| format!("pwd: cannot access '{}': {}", context.current_dir, e))
}

///
/// Display the contents of a file
/// 
fn cmd_cat(context: &mut TerminalContext, args: &[String]) -> Result<String, String> {
    if args.len() < 1 {
        return Err("cat: missing argument".to_string());
    }

    // Retrieve the target file
    let path = &args[0];
    let node_id = context.get_target_inode(path)?;

    // Ensure that the target file is a file
    if !context.fs.is_file_raw(node_id)
        .map_err(|e| format!("cat: cannot access '{}': {}", path, e))?
    {
        return Err(format!("cat: {}: Is a directory", path));
    }

    // Read the contents of the file
    let mut handle = context.fs.clone().open_raw(node_id, FileHandleType::READ)
        .map_err(|e| format!("cat: cannot access '{}': {}", path, e))?;

    // Read the whole file
    handle.seek(SeekFrom::End(0))
        .map_err(|e| format!("cat: cannot access '{}': {}", path, e))?;
    let file_size = handle.tell()
        .map_err(|e| format!("cat: cannot access '{}': {}", path, e))? as usize;
    handle.seek(SeekFrom::Start(0))
        .map_err(|e| format!("cat: cannot access '{}': {}", path, e))?;

    // Read the contents of the file
    let mut contents = vec![0; file_size];
    handle.read(&mut contents)
        .map_err(|e| format!("cat: cannot access '{}': {}", path, e))?;

    // Convert the contents to a string
    let contents = String::from_utf8_lossy(&contents).to_string();
    Ok(contents)
}

///
/// Create a new directory
/// 
fn cmd_mkdir(context: &mut TerminalContext, args: &[String]) -> Result<String, String> {
    if args.len() < 1 {
        return Err("mkdir: missing argument".to_string());
    }

    // Retrieve the target directory
    let path = &args[0];
    let (parent_dir, name) = path.rsplit_once(&['/', '\\']).unwrap_or(("", path));

    // Retrieve the parent directory
    let parent_dir = if parent_dir.is_empty() {
        context.current_dir
    } else {
        context.get_target_inode(parent_dir)?
    };

    // Ensure that the parent directory is a directory
    if !context.fs.is_directory_raw(parent_dir)
        .map_err(|e| format!("mkdir: cannot access '{}': {}", parent_dir, e))?
    {
        return Err(format!("mkdir: {}: Not a directory", parent_dir));
    }

    // Create the directory
    context.fs.mkdir_raw(parent_dir, name)
        .map_err(|e| format!("mkdir: cannot create directory '{}': {}", path, e))?;

    Ok("".to_string())
}

///
/// Create a new file
/// 
fn cmd_touch(context: &mut TerminalContext, args: &[String]) -> Result<String, String> {
    if args.len() < 1 {
        return Err("touch: missing argument".to_string());
    }

    // Retrieve the target file
    let path = &args[0];
    let (parent_dir, name) = path.rsplit_once(&['/', '\\']).unwrap_or(("", path));

    // Retrieve the parent directory
    let parent_dir = if parent_dir.is_empty() {
        context.current_dir
    } else {
        context.get_target_inode(parent_dir)?
    };

    // Ensure that the parent directory is a directory
    if !context.fs.is_directory_raw(parent_dir)
        .map_err(|e| format!("touch: cannot access '{}': {}", parent_dir, e))?
    {
        return Err(format!("touch: {}: Not a directory", parent_dir));
    }

    // Create the file
    context.fs.touch_raw(parent_dir, name)
        .map_err(|e| format!("touch: cannot create file '{}': {}", path, e))?;

    Ok("".to_string())
}

///
/// Display the help message
/// 
fn cmd_help(_context: &mut TerminalContext, _args: &[String]) -> Result<String, String> {
    let mut result = String::new();
    for (command, _) in COMMANDS.iter() {
        result.push_str(&format!("{}\n", command));
    }

    Ok(result)
}
