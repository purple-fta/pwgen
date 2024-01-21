#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include <ctype.h>
#include <stdbool.h>
#include <sys/ioctl.h>

// TODO: use terminal color shame
// TODO: Magic numbers
// TODO: Shift-Tab
// TODO: func for termios
// TODO: promPt -> promt

#define SELECT_COLOR "\e[33m"
#define UNSELECT_COLOR "\e[90m"
#define TEXT "\e[94m"
#define SEARCH_TEXT "\e[96m"
#define COUNTER_NUMBER "\e[96m"
#define COUNTER_ROW "\e[90m"
#define COUNTER_BORDER "\e[90m"


bool string_comparison(const char str1[], const char str2[]) {
    if (strlen(str1) == 0) return true;
    if (strcmp(str1, str2) == 0) return true;
    if (strcmp(str1, str2) > 0) return false;
    if (strcmp(str1, str2) < 0) {
        for (int i = 0; i < strlen(str1); i++) {
            if (str1[i] != str2[i]) return false;
        }
        return true;
    }
    return false;
}


void print_tips(int shift, int width, const char* search_text, const char* tips[], int n, int tab_index, int *tips_number, int *tips_index) {
    width -= 1;
    width -= shift;
    // clear
    for (int i = 0; i < shift+width; i++) {
        printf(" ");
    }
    printf("\e[%dD", width);
    
    printf(UNSELECT_COLOR);

    // PRINT TIPS 
    printf("[ ");
    /* printf("---%s---", tips[0]); */
    int used_width = 2;
    int d = 0;
    for (int i = 0; i < n; i++) {
        if (string_comparison(search_text, tips[i])) {
            if (used_width + strlen(tips[i]) + 3 < width ) {
                if (tab_index == d) {
                    printf("%s%s\e[0m %s| ", SELECT_COLOR, tips[i], UNSELECT_COLOR);
                    used_width += 3 + strlen(tips[i]);
                    *tips_index = i;
                } else {
                    printf("%s | ", tips[i]);
                    used_width += 3 + strlen(tips[i]);
                }
                d++;
            }
        }
    }
    if (used_width > 2) 
        printf("\e[2D] ");
    else {
        printf("\e[2D[ ]");
        used_width++;
    }
    // back cursor
    printf("\e[%dD", used_width+shift);

    *tips_number = d;
}


char* input_search(const char prompt[], const char* options[], int n) {
    struct termios old_tms, new_tms;
    int ch = ' ';
    int index = 0;
    int tab_flag = false;
    int tab_index = -1;
    int tips_number = 0;
    int tips_index = -1;

    tcgetattr(STDIN_FILENO, &old_tms);
    new_tms = old_tms;
    new_tms.c_lflag &= ~(ECHO | ICANON);
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &new_tms);

    char *input_text = malloc(sizeof(char)*150);

    for (int x = 0; x < 100; x++) {
        input_text[x] = '\0';
    }

    struct winsize w_size;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &w_size);
    int width = w_size.ws_col;

    // Print prompt
    printf("%s%s", TEXT, prompt);

    while (1) {
        ch = getchar();
        if (iscntrl(ch)) {
            if (ch == 127 && index > 0) {
                input_text[index-1] = '\0';
                printf("\e[1D \e[1D");
                index--;
                tab_flag = false;
                tab_index = -1;
                tips_index = -1;
            } else if (ch == 10) {
                if (tips_index >= 0)
                    strcpy(input_text, options[tips_index]); 
                break;
            } else if (ch == 9) {
                tab_flag = true;
                tab_index++;
                if (tab_index >= tips_number) {
                    tab_index = 0;
                }
            }
        } else {
            input_text[index] = (char)ch;
            printf("%s%c", SEARCH_TEXT, (char)ch);
            index++;
            tab_flag = false;
            tab_index = -1;
            tips_index = -1;
        }
        print_tips(1, width-strlen(prompt)-index, input_text, options, n, tab_index, &tips_number, &tips_index);
    }

    tcsetattr(STDIN_FILENO, TCSAFLUSH, &old_tms); 
    printf("\n");
    printf("\e[0m");
    
    return input_text;
}


void draw_counter_text(char prompt[], int min, int max, int counter) {
    printf(TEXT);
    printf("\r%s", prompt);
    

    if (counter > min) {
        printf(COUNTER_ROW);
        printf("<");
    } else {
        printf(COUNTER_BORDER);
        printf("|");
    }

    printf(COUNTER_NUMBER);
    printf("%d", counter);

    if (counter < max) {
        printf(COUNTER_ROW);
        printf(">");
    } else {
        printf(COUNTER_BORDER);
        printf("|");
    }
    printf("\e[0m");

}


int counter(char prompt[], int default_val, int min, int max) {
    struct termios old_tms, new_tms;
    tcgetattr(STDIN_FILENO, &old_tms);
    new_tms = old_tms;
    new_tms.c_lflag &= ~(ECHO | ICANON);
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &new_tms);

    int counter = default_val;
    char ch;
    
    printf("\e[?25l");

    draw_counter_text(prompt, min, max, counter);

    while (1) {

        ch = getchar();
        if (ch == 9) {
            if (counter < max) 
                counter++;
        } else if (ch == 10) {
            break;
        } else if (ch == 90) {
            if (counter > min)
                counter--;
        }

        printf("\e[K\e[1K");

        draw_counter_text(prompt, min, max, counter);
    }

    printf("\e[?25h");

    tcsetattr(STDIN_FILENO, TCSAFLUSH, &old_tms); 

    printf("\n");

    return counter;
}


void draw_checker_text(char prompt[], bool value) {
    printf(TEXT);
    printf("\r%s", prompt);
    
    if (value) {
        printf("%s[%sx%s]", UNSELECT_COLOR, SEARCH_TEXT, UNSELECT_COLOR);
    } else {
        printf(UNSELECT_COLOR);
        printf("[ ]");
    }
    printf("\e[0m");
}


bool checker(char prompt[], bool def_val) {
    struct termios old_tms, new_tms;
    tcgetattr(STDIN_FILENO, &old_tms);
    new_tms = old_tms;
    new_tms.c_lflag &= ~(ECHO | ICANON);
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &new_tms);

    bool val = def_val;
    char ch;

    printf("\e[?25l");

    draw_checker_text(prompt, val);
    
    while (1) {
        ch = getchar();

        if (ch == 9) {
            printf("123123123");
            val = !val;
        } else if (ch == 10) {
            break;
        }

        printf("%d-%c", ch, ch);
        printf("\e[K\e[1K");
        draw_checker_text(prompt, val);
    }

    printf("\e[?25h");

    tcsetattr(STDIN_FILENO, TCSAFLUSH, &old_tms); 

    printf("\n");

    return val;
}


