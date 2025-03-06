fn main() -> Result<(), Box<dyn std::error::Error>> {
    let user1 = User::create(101, "Alice", 500.75)?;
    user1.display()?;
    user1.save("user_data.txt")?;
    let loaded_user = User::load("user_data.txt")?;
    println!("\nLoaded User from File:");
    loaded_user.display()?;
    Ok(())
}