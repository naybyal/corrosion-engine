fn load_user(filename: &str) -> Result<User, String> {
    let file = File::open(filename).map_err(|e| e.to_string())?;
    let mut user = User::new();
    if let Err(e) = user.load(&mut BufReader::new(file)) {
        return Err(e.to_string());
    }
    Ok(user)
}