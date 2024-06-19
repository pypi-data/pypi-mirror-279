from setuptools import setup, find_packages

# Setting Up

setup(
      
      name = "pyerualjetwork",
      version = "2.3.6",
      author = "Hasan Can Beydili",
      author_email = "tchasancan@gmail.com",
      description= "Weights post process function added: [weight_post_process](optional after training before testing.), new function: manuel_balancer. And scaler_params added for scaled models.",
      packages = find_packages(),
      keywords = ["model evaluation", "classifcation", 'pruning learning artficial neural networks'],

      
      )