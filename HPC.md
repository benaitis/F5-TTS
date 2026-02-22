# Remove the symbolic link and create your own .bashrc
rm ~/.bashrc

# Copy the original content to your own .bashrc
cp /etc/qlustar/common/skel/bash/bashrc ~/.bashrc

# Now add conda to PATH
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc

# Reload
source ~/.bashrc

# Test conda
conda --version