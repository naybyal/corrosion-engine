#[derive(Debug)]
struct User {
    id: i32,
    name: String,
    balance: f64,
}
fn display_user(user: &User) {
    println!("User ID: {}", user.id);
    println!("Name: {}", user.name);
    println!("Balance: {:.2}", user.balance);
}