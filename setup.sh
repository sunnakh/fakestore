# setup.sh
pip install requests
pip install numpy
pip install pandas
pip install scikit-learn
pip install matplotlib
pip install seaborn
pip install tensorflow
pip install keras
pip install torch torchvision torchaudio
pip install transformers
pip install nltk
pip install spacy
python -m spacy download en_core_web_sm
pip install jupyterlab
pip install ipykernel
python -m ipykernel install --user --name=python_env            
# Install additional packages as needed
echo "Setup complete. You can now use the Python environment with the installed packages."
# To run this script, use: bash setup.sh