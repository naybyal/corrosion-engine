
use std::ffi::CString;
use std::os::raw::c_char;
#[derive(Debug)]
pub struct User {
    pub id: i32,
    pub name: String,
    pub balance: f32,
}
impl Drop for User {
    fn drop(&mut self) {
        println!("Dropping User: {:?}", self);
    }
}
pub fn create_user(id: i32, name: &str, balance: f32) -> Result<Box<User>, &'static str> {
    let name_cstr = CString::new(name)?;
    let mut user_buff = Vec::with_capacity(std::mem::size_of::<User>());
    user_buff.extend_from_slice(&id.to_le_bytes());
    user_buff.extend_from_slice(name_cstr.as_bytes_with_nul());
    user_buff.resize(user_buff.len() + (std::mem::size_of::<f32>() - 1), 0);
    user_buff.extend_from_slice(&balance.to_le_bytes());
    let user: User = unsafe { std::mem::transmute_copy(&user_buff) };
    Ok(Box::new(user))
}

fn display_user(user: &Option<User>) {
    if let Some(user) = user {
        println!("User ID: {}", user.id);
        println!("Name: {}", user.name);
        println!("Balance: {:.2}", user.balance);
    }
}

fn save_user(user: &User, filename: impl AsRef<Path>) -> Result<(), std::io::Error> {
    let file = File::create(filename)?;
    writeln!(&file, "{} , {} , {:.2}", user.id, user.name, user.balance)?;
    Ok(())
}

fn load_user(filename: &str) -> Result<User, String> {
    let file = File::open(filename).map_err(|e| e.to_string())?;
    let mut user = User::new();
    if let Err(e) = user.load(&mut BufReader::new(file)) {
        return Err(e.to_string());
    }
    Ok(user)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let user1 = User::create(101, "Alice", 500.75)?;
    user1.display()?;
    user1.save("user_data.txt")?;
    let loaded_user = User::load("user_data.txt")?;
    println!("\nLoaded User from File:");
    loaded_user.display()?;
    Ok(())
}

