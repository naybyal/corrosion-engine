#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define a structure to hold user details
typedef struct {
    int id;
    char name[50];
    float balance;
} User;

// Function to create a new user
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

// Function to display user details
void display_user(const User* user) {
    if (user != NULL) {
        printf("User ID: %d\n", user->id);
        printf("Name: %s\n", user->name);
        printf("Balance: %.2f\n", user->balance);
    }
}

// Function to save user data to a file
void save_user(const User* user, const char* filename) {
    FILE* file = fopen(filename, "w");
    if (file == NULL) {
        printf("Error opening file for writing\n");
        exit(1);
    }
    fprintf(file, "%d,%s,%.2f\n", user->id, user->name, user->balance);
    fclose(file);
}

// Function to read user data from a file
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

// Main function
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
