#include<iostream>
#include<vector>

using namespace std;

template <typename T>
class Kontainer
{
public:
    void add(const T& element)
    {
        container.push_back(element);
    }

    T findMin()
    {
        T minElement = container[0];
        for (const T& element : container)
        {
            if (element < minElement)
                minElement = element;
        }
        return minElement;
    }
private:
    vector<T> container;
};


int main()
{
    Kontainer<int> intContainer;
    intContainer.add(5);
    intContainer.add(3);
    intContainer.add(8);
    cout << "Minimum integer: " << intContainer.findMin() << endl;

    Kontainer<std::string> stringContainer;
    stringContainer.add("apple");
    stringContainer.add("banana");
    stringContainer.add("cherry");
    cout << "Minimum string: " << stringContainer.findMin() << endl;

    return 0;
}