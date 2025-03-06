User* load_user(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error opening file for reading\n");
        return NULL;
    }

    User* user = (User*)malloc(sizeof(User));
    if (user == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }

    fscanf(file, "%d,%49[^,],%f", &user->id, user->name, &user->balance);
    fclose(file);
    return user;
}
