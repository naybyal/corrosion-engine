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