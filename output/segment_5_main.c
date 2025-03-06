int main() {
    User* user1 = create_user(101, "Alice", 500.75);
    display_user(user1);

    save_user(user1, "user_data.txt");

    User* loaded_user = load_user("user_data.txt");
    if (loaded_user != NULL) {
        printf("\nLoaded User from File:\n");
        display_user(loaded_user);
        free(loaded_user);
    }

    free(user1);
    return 0;
}
