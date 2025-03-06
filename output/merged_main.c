

// Function to add two numbers
int add(int a, int b) {
    return a + b;
}

// Function to subtract two numbers
int subtract(int a, int b) {
    return a - b;
}

// Function to multiply two numbers
int multiply(int a, int b) {
    return a * b;
}

// Function to divide two numbers (handles division by zero)
float divide(int a, int b) {
    if (b == 0) {
        printf("Error: Division by zero!\n");
        return 0;
    }
    return (float)a / b;
}

int main() {
    int x, y, choice;
    
    printf("Enter two numbers: ");
    scanf("%d %d", &x, &y);

    printf("Choose operation:\n");
    printf("1 - Add\n2 - Subtract\n3 - Multiply\n4 - Divide\n");
    scanf("%d", &choice);

    int result;
    float result_f;
    
    switch (choice) {
        case 1:
            result = add(x, y);
            printf("Result: %d\n", result);
            break;
        case 2:
            result = subtract(x, y);
            printf("Result: %d\n", result);
            break;
        case 3:
            result = multiply(x, y);
            printf("Result: %d\n", result);
            break;
        case 4:
            result_f = divide(x, y);
            printf("Result: %.2f\n", result_f);
            break;
        default:
            printf("Invalid choice!\n");
    }

    printf("Looping through numbers 1 to 5:\n");
    for (int i = 1; i <= 5; i++) {
        printf("%d ", i);
    }
    printf("\n");

    return 0;
}

