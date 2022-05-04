# add the pip config to make installation go into the virtual environment
# make ~/.pip if doesn't exist
mkdir -p ~/.pip 
pushd ~/.pip > /dev/null
# create pip.conf if doesn't exist
touch pip.conf
if ! grep -q "[install]" "$HOME/.pip/pip.conf"; then
    echo Creating $HOME/.pip/pip.conf
    ( cat <<'EOF'
[install]
user = false
EOF
    ) >> pip.conf
fi
popd > /dev/null

# add the FLASK RUN PORT to .env if it doesn't alrady exist
if ! grep -q FLASK_RUN_PORT ".env"; then
    echo Creating .env
    echo FLASK_ENV=development >.env
    echo FLASK_RUN_PORT=5${USER: -4} >> .env
fi

# add virtual environment if it doesn't already exist
if ! [[ -d vlab ]]; then
    echo Adding virtual environment 
    python3 -m venv vlab
    source vlab/bin/activate
    echo Setting up Flask requirements
    pip install -r requirements.txt
    deactivate
fi

# activate the virtual environment for the lab
source vlab/bin/activate

# run Flask for lab1
./run.sh lab1
