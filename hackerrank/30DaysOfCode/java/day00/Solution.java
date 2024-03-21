package day00;

import java.util.Scanner;

/**
 * <strong>HackerHank</strong> challenge <strong>Day 0: Data Types</strong>, solved using <strong>java 8</strong> programming language
 *
 * <strong>Challenge</strong>
 * Save in a variable a input's line from stdin and print in output 'Hello, World' on the first line and on a second line print the variable that saved.
 *
 * @author Ed Barros / barrosef@gmail.com
 */
public class Solution {

    /**
     * Hello, World. Expression to print in this program
     */
    private static final String HELLO_WORLD_TEXT = "Hello, World.";

    /**
     * java.util.Scanner object to input interaction
     */
    private static final Scanner scanner = new Scanner(System.in);


    public static void main(String[] args) {

        System.out.println("Hello, World.");

        System.out.println(getInputText());
    }

    /**
     * Implements the interaction between our java program and scanner java.util.Scanner object.
     * @return inputed text String object
     */
    public static String getInputText() {
        String inputText = scanner.nextLine();
        scanner.close();
        return inputText;
    }
}