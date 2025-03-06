#[repr(C)]
pub struct User {
    pub id: i32,
    pub name: [u8; 50],
    pub balance: f32,
}