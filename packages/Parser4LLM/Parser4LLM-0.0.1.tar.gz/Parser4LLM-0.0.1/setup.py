from setuptools import setup, find_packages

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Parser4LLM',
    version='0.0.1',
    packages=find_packages(),
    description="""🔓📂 Unleash the Potential of Your LLMs: Effortlessly Extract Insights from PDFs, Docx, PPTX and URL! 📈💡

Supercharge your Large Language Models by converting diverse document formats into valuable, structured data. Get ready to revolutionize your AI game! 🌟🚀

""",
    author='Satish Venkatakrishnan',
    author_email='satish@askjunior.ai',
    url='https://github.com/',
    install_requires=requirements,
)