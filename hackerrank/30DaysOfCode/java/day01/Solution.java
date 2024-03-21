package day01;

import java.util.Scanner;
/**
 * <strong>HackerHank</strong> challenge <strong>Day 01: Data Types</strong>, solved using <strong>java 8</strong> programming language
 *
 * <strong>Challenge</strong>
 * Declare three different data types variables int, double and String, initialize other three same datatype variables with three stdin inputs, finally
 * - print the int initialized variable summed with first int variable
 * - print the double initialized variable summed with first double variable
 * - print the String initialized variable summed with first String variable
 *
 * @author Ed Barros / barrosef@gmail.com
 */
public class Solution {

    private static final int i = 4;
    private static final double d = 4.0;
    private static final String s = "HackerRank ";

    /**
     * Main method of the class where execution begins
     *
     * @param args command line arguments
     */
    public static void main(String[] args) {
        // Create a new scanner for reading input
        final Scanner scanner = new Scanner(System.in);
        // Read the next int and double from the user's input
        int x = scanner.nextInt();
        double j = scanner.nextDouble();
        // Consume the newline not consumed by nextDouble
        scanner.nextLine();
        // Read the next String from the user's input
        String t = scanner.nextLine();
        // Print the sum of the base number and the input number
        print(i + x);
        // Print the sum of the base double and the input double
        print(d + j);
        // Print the concatenation of the base string and the input string
        print(s.concat(t));

        scanner.close();
    }

    /**
     * Prints the provided value to the standard output.
     *
     * This method uses System.out.println to display the value of
     * the provided object. The actual output will depend on the
     * Object's toString() implementation.
     *
     * @param value The object to print to the standard output.
     */
    private static void print(Object value) {
        System.out.println(value);
    }
}
