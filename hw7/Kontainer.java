package hw7;

import java.util.ArrayList;

public class Kontainer<T extends Comparable<T>>
{
    private ArrayList<T> elements;

    public Kontainer()
    {
        elements = new ArrayList<>();
    }

    public void add(T element)
    {
        elements.add(element);
    }

    public T findMin()
    {
        T minElement = elements.get(0);
        for (T elem : elements)
        {
            if (elem.compareTo(minElement) < 0)
                minElement = elem;
        }
        return minElement;
    }

    public static void main(String[] args)
    {
        Kontainer<Double> doubleContainer = new Kontainer<>();
        doubleContainer.add(0.01);
        doubleContainer.add(-1.2);
        doubleContainer.add(3.14);
        System.out.println("Minimum Double: " + doubleContainer.findMin());

        Kontainer<String> stringContainer = new Kontainer<>();
        stringContainer.add("anna");
        stringContainer.add("apple");
        stringContainer.add("carey");
        System.out.println("Minimum String: " + stringContainer.findMin());
    }
}
