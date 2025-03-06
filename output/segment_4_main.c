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
