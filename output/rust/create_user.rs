#[derive(Debug)]
struct User {
    id: i32,
    name: String,
    balance: f32,
}
fn create_user(id: i32, name: &str, balance: f32) -> User {
    User {
        id,
        name: {
            let mut truncated_name = name.to_string();
            truncated_name.truncate(255); // Assuming a 256-char buffer in C, leave space for null
            truncated_name
        },
        balance,
    }
}