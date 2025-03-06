use std::io;
fn add(x: i32, y: i32) -> i32 {
    x + y
}
fn subtract(x: i32, y: i32) -> i32 {
    x - y
}
fn multiply(x: i32, y: i32) -> i32 {
    x * y
}
fn divide(x: i32, y: i32) -> f32 {
    if y == 0 {
        f32::NAN
    } else {
        x as f32 / y as f32
    }
}
fn main() {
    let mut x = String::new();
    let mut y = String::new();
    println!("Enter two numbers: ");
    io::stdin().read_line(&mut x).expect("Failed to read line");
    io::stdin().read_line(&mut y).expect("Failed to read line");
    let x: i32 = x.trim().parse().expect("Please type a number!");
    let y: i32 = y.trim().parse().expect("Please type a number!");
    println!("Choose operation:");
    println!("1 - Add\n2 - Subtract\n3 - Multiply\n4 - Divide");
    let mut choice = String::new();
    io::stdin()
        .read_line(&mut choice)
        .expect("Failed to read line");
    let choice: i32 = choice.trim().parse().expect("Please type a number!");
    match choice {
        1 => {
            let result = add(x, y);
            println!("Result: {}", result);
        }
        2 => {
            let result = subtract(x, y);
            println!("Result: {}", result);
        }
        3 => {
            let result = multiply(x, y);
            println!("Result: {}", result);
        }
        4 => {
            let result_f = divide(x, y);
            println!("Result: {:.2}", result_f);
        }
        _ => {
            println!("Invalid choice!");
        }
    }
    println!("Looping through numbers 1 to 5:");
    for i in 1..=5 {
        print!("{} ", i);
    }
    println!();
}