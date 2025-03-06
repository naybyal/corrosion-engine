void save_user(const User* user, const char* filename) {
    FILE* file = fopen(filename, "w");
    if (file == NULL) {
        printf("Error opening file for writing\n");
        exit(1);
    }
    fprintf(file, "%d,%s,%.2f\n", user->id, user->name, user->balance);
    fclose(file);
}
