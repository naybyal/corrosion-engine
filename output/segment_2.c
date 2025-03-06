void display_user(const User* user) {
    if (user != NULL) {
        printf("User ID: %d\n", user->id);
        printf("Name: %s\n", user->name);
        printf("Balance: %.2f\n", user->balance);
    }
}
