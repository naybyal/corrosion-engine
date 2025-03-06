use std::fs::File;
use std::io::Write;
use std::path::Path;
#[derive(Debug)]
struct User<'a> {
    id: i32,
    name: &'a str,
    balance: f64,
}
fn save_user(user: &User, filename: &str) -> std::io::Result<()> {
    let path = Path::new(filename);
    let mut file = File::create(&path)?;
    write!(file, "{},{},{:.2}\n", user.id, user.name, user.balance)?;
    Ok(())
}