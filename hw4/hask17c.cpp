#include <vector>
#include <algorithm>
#include <iostream>

using namespace std;

class Tree {
public:
    unsigned value;
    vector<Tree *> children;

    Tree(unsigned value, vector<Tree *> children) {
        this->value = value;
        this->children = children;
    }
};

int maxTreeValue(Tree* root) {
    if (root == nullptr)
        return 0;

    vector<Tree*> q;
    q.push_back(root);
    int maxValue = 0;

    while (q.size() != 0) {
        Tree* node = q.front();
        q.pop_back();

        maxValue = max(maxValue, int(node->value));
        for (Tree* c : node->children) {
            q.push_back(c);
        }
    }

    return maxValue;
}

int main() {
    Tree* leaf1 = new Tree(5, {});
    Tree* leaf2 = new Tree(3, {});
    Tree* child1 = new Tree(10, {leaf1, leaf2});
    Tree* root = new Tree(7, {child1});

    unsigned result = maxTreeValue(root);
    cout << "Max value in tree: " << result << endl;  // Output: 10

    delete leaf1;
    delete leaf2;
    delete child1;
    delete root;

    return 0;
}
