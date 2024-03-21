package day02;

import java.util.Scanner;

/**
 * The Solution class implements a solution for the Day 02 challenge
 * from the 30 Days of Code tutorial on HackerRank, using Java 15+.
 * It calculates the total cost of a meal, given the meal cost,
 * tip percentage, and tax percentage.
 */
public class Solution {

    /**
     * Constant variable to be used while performing calculations.
     */
    private static final double ONE_HUNDRED = 100;

    /**
     * Messages for invalid inputs.
     */
    private static final String INVALID_DOUBLE_MESSAGE = "Invalid input! Please enter a double value.";
    private static final String INVALID_INT_MESSAGE = "Invalid input! Please enter a integer value.";

    /**
     * Scanner instance for taking user inputs.
     */
    private static Scanner in = new Scanner(System.in);

    /**
     * The main method where the program execution starts.
     * @param args The command line arguments.
     */
    public static void main(String[] args) {

        double mealCost = fetchDoubleInput();
        int tipPercent = fetchIntInput();
        int taxPercent = fetchIntInput();

        double tipCost = calculatePercentage(mealCost, tipPercent);
        double taxCost = calculatePercentage(mealCost, taxPercent);
        long totalCost = calculateTotalCost(mealCost, tipCost, taxCost);

        printMessage(totalCost);

        closeIn();
    }

    /**
     * Calculates the total cost of the meal.
     * @param mealCost The base cost of the meal.
     * @param tipCost  The calculated tip cost.
     * @param taxCost  The calculated tax cost.
     * @return The total cost rounded to the nearest whole number.
     */
    private static long calculateTotalCost(double mealCost, double tipCost, double taxCost) {
        return Math.round(mealCost + tipCost + taxCost);
    }

    /**
     * Calculates a percentage of a given value.
     * @param value   The base value.
     * @param percent The percent to calculate.
     * @return The calculated percentage of the base value.
     */
    private static double calculatePercentage(double value, int percent) {
        return value * (percent / ONE_HUNDRED);
    }

    /**
     * Utility function to handle input of type double.
     * @return The user input as a double value.
     */
    private static double fetchDoubleInput() {
        while (!in.hasNextDouble()){
            printMessage(INVALID_DOUBLE_MESSAGE);
            in.next();
        }
        return in.nextDouble();
    }

    /**
     * Utility function to handle input of type integer.
     * @return The user input as an integer.
     */
    private static int fetchIntInput() {
        while (!in.hasNextInt()){
            printMessage(INVALID_INT_MESSAGE);
            in.next();
        }
        return in.nextInt();
    }

    /**
     * Prints a given message to the standard output.
     * @param message The message to be printed.
     */
    private static void printMessage(Object message) {
        System.out.println(message);
    }

    /**
     * Closes the Scanner instance.
     */
    private static void closeIn() {
        in.close();
    }

}