from evaluation_scripts.tl_manager_adapter import *

if __name__ == "__main__":
    trees = get_trees()

    for (tree_name, size) in trees.items():
        print(f'Creating {tree_name} with size {size}')
        tree = create_tree(tree_name, 2048)

        for i in range(0, size):
            insert_leaf(tree_name, str(i))
            print(f'{i} of {size}', end='\r')
        commit_tree(tree_name)
        print('')
