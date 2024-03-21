package day02;

import java.util.Scanner;

public class Solution {
    public static void main(String[] args) {


        Scanner in = new Scanner(System.in);

        double meal_cost = in.nextDouble();
        int tip_percent = in.nextInt();
        int tax_percent = in.nextInt();

        double tip_cost = meal_cost * (tip_percent / 100);
        double tax_cost = meal_cost * (tax_percent / 100);

        long total_cost = Math.round(meal_cost + tip_cost + tax_cost);

        System.out.println("The total meal cost is " + total_cost +" dollars.");

        in.close();
    }
}
