#![allow(non_camel_case_types)]
#![allow(dead_code)]
use std::fs::File;
use std::io::{BufReader, Read};
use std::path::Path;
#[derive(Debug, Default)]
#[repr(C)]
pub struct User {
    id: i32,
    name: [u8; 50],
    balance: f32,
}
fn load_user(filename: &str) -> Option<Box<User>> {
    let path = Path::new(filename);
    let file = match File::open(&path) {
        Ok(file) => file,
        Err(_) => {
            eprintln!("Error opening file for reading");
            return None;
        }
    };
    let mut reader = BufReader::new(file);
    let mut contents = String::new();
    if let Err(e) = reader.read_to_string(&mut contents) {
        eprintln!("Error reading file: {}", e);
        return None;
    }
    let mut user = Box::new(User::default());
    let parts: Vec<&str> = contents.trim().split(',').collect();
      if parts.len() != 3 {
        eprintln!("Invalid file format");
        return None;
    }
    user.id = match parts[0].parse() {
        Ok(id) => id,
        Err(_) => {
          eprintln!("Error parsing user ID");
          return None
        }
    };
    let name_bytes = parts[1].as_bytes();
    let name_len = std::cmp::min(name_bytes.len(), user.name.len() -1);
    user.name[..name_len].copy_from_slice(&name_bytes[..name_len]);
    user.name[name_len] = 0; //null terminate
    user.balance = match parts[2].parse() {
        Ok(balance) => balance,
        Err(_) => {
          eprintln!("Error parsing user balance");
          return None;
        }
    };
    Some(user)
}