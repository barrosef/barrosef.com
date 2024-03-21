package day02;

import java.util.Scanner;

public class Solution {
    private static Scanner in = new Scanner(System.in);
    private static final double ONE_HUNDRED = 100;
    public static void main(String[] args) {
        double mealCost = in.nextDouble();
        int tipPercent = in.nextInt();
        int taxPercent = in.nextInt();

        double tipCost = getValueFromPercent(mealCost, tipPercent);
        double taxCost = getValueFromPercent(mealCost, taxPercent);

        long totalCost = solve(mealCost, tipCost, taxCost);

        System.out.println(totalCost);

        in.close();
    }

    private static long solve(double mealCost, double tipCost, double taxCost) {
        return Math.round(mealCost + tipCost + taxCost);
    }

    static double getValueFromPercent(double value, double percent) {
        return value * (percent / ONE_HUNDRED);
    }
}
