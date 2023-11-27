import random
import sys
import unittest
import matplotlib.pyplot as plt

def generate_synthetic_data(categories: list[tuple[str, int]], num_samples: int) -> list[str]:
    """
    Generate synthetic data

    The categories are weighted by expected frequency.

    :param categories: tuple of category to weight
    :param num_samples: number of samples
    :return: list of str
    """
    # first convert the above into a distribution
    total_frequency = sum([c[1] for c in categories])
    categories_distribution = [(c[0], c[1] / total_frequency) for c in categories]
    category_names = [c[0] for c in categories_distribution]
    category_probability = [c[1] for c in categories_distribution]
    data = random.choices(category_names, category_probability, k=num_samples)
    return data


def group_data(data, reverse=True) -> list[tuple[str, int]]:
    """
    Group the data by category

    :param data: raw instances of categorical data
    :param reverse: sort in descending order
    :return: list of tuples of str, int
    """
    categories = list(set(data))
    return sorted([(category, data.count(category)) for category in categories], key=lambda x: x[1], reverse=reverse)


def pareto_chart(data: list[tuple[str, int]]) -> None:
    """
    Plot a pareto chart using matplotlib
    :param data:
    :return:
    """
    print(f"{data = }")
    # create the plot
    fig, ax1 = plt.subplots()
    categories = [c[0] for c in data]
    counts = [c[1] for c in data]
    # plot the bars
    ax1.bar(
        categories,
        counts,
        align='center',
        color='green',
        edgecolor='black',
        width=0.5,
    )
    # plot the cumulative sum
    total = sum(counts)
    cumsum = list()
    for i, count in enumerate(counts):
        if i == 0:
            cumsum.append(count)
        else:
            cumsum.append(count + cumsum[-1])
    print(f"{cumsum = }")
    percent_cumsum = [c / total * 100 for c in cumsum]
    print(f"{percent_cumsum = }")
    ax2 = ax1.twinx()
    ax2.plot(
        categories,
        percent_cumsum,
        color='red',
        marker='o',
    )
    # set the ticks
    ax1.set_xticks(categories)
    ax1.set_xticklabels(categories)
    # set the labels
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Count')
    ax2.set_ylabel('Cumulative Count')
    ax2.set_ylim(0, 110)
    ax2.hlines(80, 0, len(categories), colors='red', linestyles='dashed')
    # set the title
    ax1.set_title('Pareto Chart')
    # show the plot
    plt.show()


def main():
    # generate synthetic data
    # the data is structured as follows: a list of tuples each
    # with an ID and a categorical variable (e.g. 'A', 'B', 'C')
    _categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    _frequency = [37, 7, 5, 4, 3, 2, 1, 1, 1]
    random.shuffle(_frequency)
    categories = list(zip(_categories, _frequency))
    num_samples = 1000
    data = generate_synthetic_data(categories, num_samples)
    grouped_data = group_data(data)
    # create pareto chart
    pareto_chart(grouped_data)
    return 0


if __name__ == '__main__':
    sys.exit(main())


# unit tests
class Tests(unittest.TestCase):
    def test_generate_synthetic_data(self):
        data = generate_synthetic_data(list(zip(['A', 'B', 'C'], [1, 5, 10])), 10)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 10)
        self.assertIsInstance(data[0], str)

    def test_statistics(self):
        categories = [('A', 37), ('B', 7)]
        print(f"{categories = }")
        # first convert the above into a distribution
        total_frequency = sum([c[1] for c in categories])
        categories_distribution = [(c[0], c[1] / total_frequency) for c in categories]
        category_names = [c[0] for c in categories_distribution]
        category_probability = [c[1] for c in categories_distribution]
        print(f"{categories_distribution = }")
        print(f"{category_names = }")
        print(f"{category_probability = }")
        choices = random.choices(category_names, category_probability, k=10)
        print(f"{choices = }")

    def test_group_data(self):
        data = generate_synthetic_data(list(zip(['A', 'B', 'C'], [1, 5, 10])), 100)
        print(f"{data = }")
        grouped_data = group_data(data, reverse=True)
        print(f"{grouped_data = }")
        self.assertEqual(len(grouped_data), 3)
        self.assertIsInstance(grouped_data, list)
        self.assertIsInstance(grouped_data[0], tuple)
        self.assertEqual(len(grouped_data[0]), 2)
        self.assertIsInstance(grouped_data[0][0], str)
        self.assertIsInstance(grouped_data[0][1], int)
        grouped_data = group_data(data, reverse=False)
        print(f"{grouped_data = }")
        self.assertTrue(grouped_data[0][1] < grouped_data[-1][1])
