from aitextgen import aitextgen

ai = aitextgen(model_folder="../site", )

projects = ai.generate(n=100, return_as_list=True)
