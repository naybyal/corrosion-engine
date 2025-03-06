fn save_user(user: &User, filename: impl AsRef<Path>) -> Result<(), std::io::Error> {
    let file = File::create(filename)?;
    writeln!(&file, "{} , {} , {:.2}", user.id, user.name, user.balance)?;
    Ok(())
}