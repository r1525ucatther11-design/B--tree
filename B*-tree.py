import random
import time
import csv

class BStarNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

class BStarTree:
    def __init__(self, t=3):
        self.t = t
        self.root = BStarNode(t, True)
        self.steps = 0

    def reset_steps(self):
        self.steps = 0


    def search(self, k, node=None):
        if node is None:
            node = self.root

        self.steps += 1

        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
            self.steps += 1

        if i < len(node.keys) and node.keys[i] == k:
            return True

        if node.leaf:
            return False

        return self.search(k, node.children[i])


    def insert(self, k):
        if self.search(k):
            return

        root = self.root

        if len(root.keys) == 2 * self.t - 1:
            new_root = BStarNode(self.t, False)
            new_root.children.append(root)
            self.root = new_root
            self._split_child(new_root, 0)

        self._insert_non_full(self.root, k)

    def _insert_non_full(self, node, k):
        self.steps += 1

        i = len(node.keys) - 1

        if node.leaf:
            node.keys.append(0)

            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
                self.steps += 1

            node.keys[i + 1] = k

        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
                self.steps += 1

            i += 1

            self._insert_non_full(node.children[i], k)


    def _split_child(self, parent, i):
        t = self.t

        node = parent.children[i]
        new_node = BStarNode(t, node.leaf)
        mid = node.keys[t - 1]

        new_node.keys = node.keys[t:]
        node.keys = node.keys[:t - 1]

        if not node.leaf:
            new_node.children = node.children[t:]
            node.children = node.children[:t]

        parent.children.insert(i + 1, new_node)
        parent.keys.insert(i, mid)

        self.steps += 1


    def delete(self, k):
        self._delete(self.root, k)

        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def _delete(self, node, k):
        self.steps += 1

        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
            self.steps += 1

        if i < len(node.keys) and node.keys[i] == k:

            if node.leaf:
                node.keys.pop(i)
                return
            else:
                pred = self._get_pred(node.children[i])
                node.keys[i] = pred
                self._delete(node.children[i], pred)

        else:
            if node.leaf:
                return
            self._delete(node.children[i], k)

    def _get_pred(self, node):
        while not node.leaf:
            node = node.children[-1]
            self.steps += 1
        return node.keys[-1]


tree = BStarTree(t=3)

data = random.sample(range(1, 1_000_000), 10_000)
with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["value"])  # заголовок столбца
    for x in data:
        writer.writerow([x]) # для отчета

# insert test
insert_results = []

for x in data:
    tree.reset_steps()

    start = time.perf_counter()
    tree.insert(x)
    end = time.perf_counter()

    insert_results.append([end - start, tree.steps])

# search test (100 элементов)
search_results = []

search_data = random.sample(data, 100)

for x in search_data:
    tree.reset_steps()

    start = time.perf_counter()
    tree.search(x)
    end = time.perf_counter()

    search_results.append([end - start, tree.steps])

# delete test (1000 элементов)
delete_results = []

delete_data = random.sample(data, 1000)

for x in delete_data:
    tree.reset_steps()

    start = time.perf_counter()
    tree.delete(x)
    end = time.perf_counter()

    delete_results.append([end - start, tree.steps])

def save_csv(filename, data):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_sec", "steps"])
        writer.writerows(data)


save_csv("insert_results.csv", insert_results)
save_csv("search_results.csv", search_results)
save_csv("delete_results.csv", delete_results)

# стреднее
def avg(col):
    return sum(col) / len(col)

insert_time = avg([x[0] for x in insert_results])
insert_steps = avg([x[1] for x in insert_results])

search_time = avg([x[0] for x in search_results])
search_steps = avg([x[1] for x in search_results])

delete_time = avg([x[0] for x in delete_results])
delete_steps = avg([x[1] for x in delete_results])


print("\nAVERAGE RESULTS:")

print("Insert:", insert_time, insert_steps)
print("Search:", search_time, search_steps)
print("Delete:", delete_time, delete_steps)
