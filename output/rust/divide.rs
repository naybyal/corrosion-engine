fn divide(a: i32, b: i32) -> f32 {
    if b == 0 {
        println!("Error: Division by zero!");
        return 0.0;
    }
    a as f32 / b as f32
}