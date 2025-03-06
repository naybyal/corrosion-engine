fn display_user(user: &Option<User>) {
    if let Some(user) = user {
        println!("User ID: {}", user.id);
        println!("Name: {}", user.name);
        println!("Balance: {:.2}", user.balance);
    }
}