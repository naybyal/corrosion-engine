User* create_user(int id, const char* name, float balance) {
    User* user = (User*)malloc(sizeof(User));
    if (user == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    user->id = id;
    strncpy(user->name, name, sizeof(user->name) - 1);
    user->name[sizeof(user->name) - 1] = '\0';
    user->balance = balance;
    return user;
}
