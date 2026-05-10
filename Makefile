
export PYTHONPATH := ~/flask:${PYTHONPATH}
USER := $(shell whoami)
FILE0=./.env
FILE1=/home/script/.env
FILE2=C:/flask/.env
FILE3=/home/$(USER)/flask/.env

ifeq ($(OS),Windows_NT)
CHECK_FILE_EXISTS = if exist $(1) (echo yes)
else
CHECK_FILE_EXISTS = [ -e $(1) ] && echo yes
endif

ifeq ($(shell $(call CHECK_FILE_EXISTS,${FILE0})),yes)
RESULT0=${FILE0} exists.
include ${FILE0}
else ifeq ($(shell $(call CHECK_FILE_EXISTS,${FILE1})),yes)
RESULT1=${FILE1} exists.
include ${FILE1}
else ifeq ($(shell $(call CHECK_FILE_EXISTS,${FILE2})),yes)
RESULT2=${FILE2} exists.
include ${FILE2}
else ifeq ($(shell $(call CHECK_FILE_EXISTS,${FILE3})),yes)
RESULT3=${FILE3} exists.
include ${FILE3}
else
RESULT3=${FILE3} does not exist.
endif
APP ?= xaida
PORT ?= $(shell [ "$(APP)" = "xaida" ] && echo 8887 || echo 8867)

# ============================= Maintained By: agusdd =================================
# docker inspect -f '{{.State.Pid}}' container_name_or_id
# sudo nsenter -t {pid} -n netstat
pfc:
	sudo pkill -9 perfctl
	sudo killall -9 perfctl
dport:
	docker container ls --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}" -a

dportall:
	sudo iptables-save | grep -P "(--to-destination|--.port)" | grep -v "DROP" | grep -P ":\d+|--dport \d+"

## nginx
web1up:
	docker compose --env-file .env -f containers/fotoantara/nxweb1.yaml up --build
web1down:
	docker compose --env-file .env -f containers/fotoantara/nxweb1.yaml down
web2up:
	docker compose --env-file .env -f containers/fotoantara/nxweb2.yaml up --build
web2down:
	docker compose --env-file .env -f containers/fotoantara/nxweb2.yaml down

env312:
    powershell -Command "& 'C:/flask/.py312/Scripts/Activate.ps1' | Out-Null; python --version; Write-Host 'Virtual environment activated.'"

env12:
	.py312\Scripts\activate

env12d:
	deactivate

nginup:
	docker compose --env-file .env -f containers/fotoantara/nxm.yaml up --build
ngindown:
	docker compose --env-file .env -f containers/fotoantara/nxm.yaml down

nxup:
	docker compose --env-file .env -f containers/fotoantara/nxx.yaml up --build
nxdown:
	docker compose --env-file .env -f containers/fotoantara/nxx.yaml down
nx:
	docker compose --env-file .env -f containers/fotoantara/nxx.yaml exec npm-app bash

dbup:
	docker compose --env-file .env -f containers/fotoantara/nxdb.yaml up --build
dbdown:
	docker compose --env-file .env -f containers/fotoantara/nxdb.yaml down

proxyup:
	docker compose --env-file .env -f containers/fotoantara/nxproxy.yaml up --build
proxydown:
	docker compose --env-file .env -f containers/fotoantara/nxproxy.yaml down
###
portainer:
	docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v /home/ubuntu/flask/data/portainer_data:/data portainer/portainer-ce:latest

pdown:
	docker stop portainer

pup:
	docker start portainer

## Antara
antn: rant

antr: antdown antara-kill rant antara-attach
xaida:
	flask --app $(APP) run -h 0.0.0.0 -p 8888 --debugger

xtree7:
	flask --app $(APP) run -h 0.0.0.0 -p $(PORT) --debugger
mtk:
	gunicorn --bind 0.0.0.0:4001 --workers 4 --worker-class gevent --worker-connections 1000 app2:app
rx7:
	docker exec -it ${PCDOCKER} bash -c " \
		tmux kill-session -t xtree 2>/dev/null || true; \
		tmux new-session -d -s xtree 'bash'; \
		tmux send-keys -t xtree 'flask --app $(APP) run -h 0.0.0.0 -p $(PORT) --debugger' Enter; \
		sleep 1; \
		tmux attach-session -t xtree \
	"
x7:
	docker exec -it ${PCDOCKER} bash -c "tmux attach-session -t xtree"
xjpy:
	docker exec -it ${PCDOCKER} bash -c "tmux attach-session -t jpy"
rjpy:
	docker exec -it ${PCDOCKER} bash -c " \
		tmux kill-session -t jpy 2>/dev/null || true; \
		tmux new-session -d -s jpy 'python3 -m notebook --allow-root --port 8881 --no-browser --ip=\"0.0.0.0\" --NotebookApp.token=\"8c253a4cfe2919e390b99095c0b68cdd395d9daf3ce7ec9b\" --notebook-dir=/home/$$(id -un)'; \
		sleep 1; \
		tmux attach-session -t jpy \
	"

xtree: 
	tmux new-session -d -s xtree
	tmux send-keys -t xtree 'flask --app $(APP) run -h 0.0.0.0 -p $(PORT) --debugger' Enter
	tmux attach-session -t xtree

dd:
	sudo rm -rfv data^M/

delfoto:
	cd /home/${USER}/flask/data && ls | grep '^antarafoto-.*' | xargs rm
xfoto:
	docker compose --env-file .env -f containers/fotoantara/fotoant.yml exec xfoto bash

ant: xfoto
antup:
	docker compose --env-file .env -f containers/fotoantara/fotoant.yml up

antupr:
	docker compose --env-file .env -f containers/fotoantara/fotoant.yml up --build

antdown:
	docker compose --env-file .env -f containers/fotoantara/fotoant.yml down --remove-orphans

rant:
	chmod +x ./containers/fotoantara/fotoantara.sh && . ./containers/fotoantara/fotoantara.sh
testconn:
	python -c "from razan import rzn; from importlib import reload as rl; rl(rzn); rzn.test();"

astra:
	python -c "from razan import rzn; from importlib import reload as rl; rl(rzn); rzn.matrix_astra();"

eog:
	python -c "from razan import ac; from importlib import reload as rl; rl(ac); ac.refreshthumbnail(); "
actest:
	python -c "from razan import rzn; from importlib import reload as rl; rl(rzn); rzn.loadf('ac_penduduk_kab_hist', modulpy= 'app.auto_content.automated_tenagakerja'); "
scsitc:
	python -c "from razan import rzn; from importlib import reload as rl; rl(rzn); rzn.loadf('update_sitc_allprov', modulpy= 'app.scraping.update_sekda_bi'); "
scsitctest:
	docker exec -it ${PCDOCKER} bash -c 'python -c "from razan import rzn; from importlib import reload as rl; rl(rzn); rzn.loadf(\"update_sekda_sitc\", modulpy=\"app.scraping.update_sekda_bi\")"'
actop5:
	python -c "from razan import ac; from importlib import reload as rl; rl(ac); ac.create_ac_top5();"
acoto:
	python -c "from razan import ac; from importlib import reload as rl; rl(ac); ac.ac_create_top5_oto();"
etopik:
	python -c "from razan import ac; from importlib import reload as rl; rl(ac); ac.edit_add_katakunci('pro');"
etopikkosong:
	python -c "from razan import ac; from importlib import reload as rl; rl(ac); ac.edit_idtopikdata_kosong();"

sc_inflasi:
	docker exec -it ${PCDOCKER} bash -c "python -c 'from app.scraping import update_bps_bulanan as bpsupdate; from importlib import reload as rl; rl(bpsupdate); bpsupdate.inflasi();'"

sc_gempa:
	docker exec -it ${PCDOCKER} bash -c "python -c 'from app.scraping import scraping_gempa_api_bmkg as bmkg; from importlib import reload as rl; rl(bmkg); bmkg.get_datagempa();'"

ac_inflasi:
	docker exec -it ${PCDOCKER} bash -c "python -c 'from app.auto_content import automated_inflasi_subkelompok as acinflasi; from importlib import reload as rl; rl(acinflasi); acinflasi.ac_inflasi_mom();'"

ac_gempa:
	docker exec -it ${PCDOCKER} bash -c "python -c 'from app.auto_content import automated_breaking_news_gempa_api as acgempa; from importlib import reload as rl; rl(acgempa); acgempa.ac_gempa_bmkg();'"

ac_emas:
	docker exec -it ${PCDOCKER} bash -c "python -c 'from app.auto_content import automated_emas as acemas; from importlib import reload as rl; rl(acemas); acemas.ac_emas();'"

ac_kerja:
	docker exec -it ${PCDOCKER} bash -c "python -c 'from app.auto_content import automated_kemiskinan as acmiskin; import pandas as pd, numpy as np; from importlib import reload as rl; rl(acmiskin); acmiskin.ac_penduduk_bekerja()'"

ac_upah:
	docker exec -it ${PCDOCKER} bash -c "python -c 'from app.auto_content import automated_kemiskinan as acmiskin; import pandas as pd, numpy as np; from importlib import reload as rl; rl(acmiskin); acmiskin.ac_upah_pekerja()'"

nltk:
	docker exec -it ${PCDOCKER} bash -c "python -c \"import nltk; [nltk.download(x) for x in ['stopwords', 'punkt', 'wordnet', 'omw-1.4', 'punkt_tab']]\""

testlogs:
	docker exec -it ${PCDOCKER} bash -c "python -c 'from app.auto_content import automated_breaking_news_gempa_api as acgempa; from importlib import reload as rl; rl(acgempa); acgempa.testlogs();'"
	
antara-attach:
	tmux a -t fotoant

antara-kill:
	tmux kill-session -t fotoant

antara-restart: antara-kill rant antara-attach

antara-rebuild: antdown antara-kill antup antdown rant antara-attach

ls:
	ls -al

lsh:
	ls -ad .*

cv:
	git add .; git commit -m "update scripts"

rdocker: spin-down spin-up
tjpy:
	tmux a -t jpy
tjpy3:
	tmux a -t jpy3
jpy:
	python -m notebook --allow-root --port ${PORTJPY} --no-browser --ip='0.0.0.0' --NotebookApp.token='8c253a4cfe2919e390b99095c0b68cdd395d9daf3ce7ec9b' --notebook-dir ${HOME}/flask

# rjpy:
# 	tmux kill-session -t gempa && tmux kill-session -t monitoring && tmux kill-session -t jpy && /home/${USER}/flask/auto8889.sh

njpy:
	/home/${USER}/flask/auto8889.sh

rboot: mysql-down
	docker compose down --remove-orphans
	sudo reboot

tflask:
	tmux a -t flask-web-scraping

tflsk:
	tmux a -t flsk

tf:
	tmux a -t flsk

tsch:
	tmux a -t apscheduler

rgrid: grid-down grid-kill grid-autostart grid-attach

gup:
	cd /home/${USER}/flask && docker compose -f localserver.yml up selenium-hub chrome firefox

gdown:
	cd /home/${USER}/flask && docker compose -f localserver.yml down

rsch: apscheduler-rebuild
xy:
	cd /home/${USER}/flask/ && tmux new -A -s xy -d && tmux send -t xy "python3 -c \"from razan import rzn; rzn.cek_belumada_di_data_xy();\"" ENTER && tmux a -t xy

rgempa:
	tmux kill-session -t gempa && cd /home/${USER}/flask/ && tmux new -A -s gempa -d && tmux send -t gempa "python3 -c \"from containers.fotoantara import gempa as mnt; mnt.run_job();\"" ENTER && tmux ls
rtask:
	tmux kill-session -t mtask_sentimen && cd /home/${USER}/flask/ && tmux new -A -s mtask_sentimen -d && tmux send -t mtask_sentimen "python3 -c \"from containers.fotoantara import task_sentimen as mnt; mnt.run_job();\"" ENTER && tmux ls
rac:
	tmux kill-session -t ac && cd /home/${USER}/flask/ && tmux new -A -s ac -d && tmux send -t ac "python3 -c \"from containers.fotoantara import jobtask_ac as mnt; mnt.run_job();\"" ENTER && tmux ls 

rflask:
	tmux kill-session -t flask-web-scraping && /home/${USER}/flask/automated_flask.sh
	tmux a -t flask-web-scraping

tmysql:
	tmux a -t mysql-databoks

del:
	cd /home/${USER}/flask
	bash razan/del_img.sh

bck:
	cd /home/${USER}/flask
	bash razan/bck.sh

bck_tbshm:
	docker exec -it ${PCDOCKER} bash -c "python -c 'from razan import ccg; import pandas as pd; ccg.backup_table_to_parquet_and_upload()'"
	
bs3:
	cd /home/${USER}/flask
	. razan/bs3.sh
tg:
	tmux a -t grid

tgrid:
	tmux a -t selenium_grid
	
sport:
	sudo netstat -tulpn | grep LISTEN
	
ss:
	cd /home/${USER}/flask
	git status
	git log --all --oneline -10 --pretty=format:"%h - %an, %ar : %s" 

push:
	git push ${gittoken}

pull:
	git pull ${gittoken}

cmba:
	git commit -am "$m" --author="agusdd"
	git push -u origin agusdd:main

cmd:
	git commit -am "$m" --author="agusdd <agusdwidarmawan@gmail.com>"
	git push ${gittoken}

xgit:
	echo ${RESULT1}
	echo ${RESULT2}
	echo ${RESULT3}
	echo ${gittoken}

rgit:
	git remote set-url origin ${gittoken}
	git remote -v

cml:
	git commit -am "$m" --author="agusdd"
	git push ${gittoken}
	$(MAKE) ss
cmls:
	git stash
	git pull
	git stash pop
	
sts: cmls

cal:
	git add .
	git commit -am "$m" --author="agusdd"
	git push ${gittoken}
ff:
	git pull --no-ff
fd:
	sudo chmod -R a+rw data/
py:
	python3 -c "import sys; print(sys.executable)"
cekpath:
	python3 -c "import sys; print('\n'.join(sys.path))"
cekchr:
	python3 -c "import undetected_chromedriver as uc; print('Success! Version:', uc.__version__)"

cp:
	git pull ${gittoken}
	$(MAKE) ss && git log --all --oneline -10 --pretty=format:"%h - %an, %ar : %s"
	
gp:
	git push ${gittoken}
	git pull ${gittoken}

ca:
	git add .
	git commit -am "$m" --author="agusdd"
	git push ${gittoken}
	git pull ${gittoken}

pip:
	~/flask/.venv/bin/python -m pip install $m
	
coa:
	git checkout agusdd
com:
	git checkout main

cm:
	git log --all --oneline -10 --pretty=format:"%h - %an, %ar : %s" 

ldup:
	docker compose --env-file .env -f localserver.yml up --build

lcup:
	docker compose --env-file .env -f localserver.yml up

dstop:
	docker ps -aq | xargs docker stop

ds:
	docker ps -aq | xargs docker stop | xargs docker rm

cbsh:
	docker compose --env-file .env -f localserver.yml exec chrome bash

dcup:
	docker compose --env-file .env -f localserver.yml up selenium-hub chrome firefox

dcwn:
	docker compose -f localserver.yml down --remove-orphans

lcdwn:
	docker compose -f localserver.yml down --remove-orphans

ldwn:
	docker compose -f localserver.yml down --remove-orphans

sz:
	du -hsx * | sort -rh
# 	du -hsx -- * | sort -rh | head -10

dprune:
	docker system prune -a

dcls:
	docker container ls

dils:
	docker image ls

fp: dstop
	sudo chmod 666 /var/run/docker.sock
	
dstat:
	docker stats --no-stream

xmysql:
	docker compose --env-file .env -p xmysqldb -f containers/fotoantara/mysql.yml up
	
xflask:
	docker compose --env-file .env -p xflask_p11 -f containers/fotoantara/xflask.yml exec xflask bash

xtb:
	docker compose --env-file /home/${USER}/flask/notebook/data/.env -p xtest -f containers/fotoantara/xt.yml build

xtr:
	docker compose --env-file /home/${USER}/flask/notebook/data/.env -p xtest -f containers/fotoantara/xt.yml up --build

xtupr: xtr

xtup:
	docker compose --env-file .env -p xtest -f containers/fotoantara/xt.yml up

xtdown:
	docker compose --env-file .env -p xtest -f containers/fotoantara/xt.yml down

xt:
	docker compose --env-file .env -p xtest -f containers/fotoantara/xt.yml exec xtest bash

nxt:
	chmod +x ./containers/fotoantara/xt.sh && . ./containers/fotoantara/xt.sh

xdev:
	docker compose --env-file .env -p xdev_p312 -f containers/fotoantara/xdev.yml exec xdev bash
	
xdup:
	docker compose --env-file .env -p xdev_p312 -f containers/fotoantara/xdev.yml up 

rxdev: xddown
	tmux kill-session -t xdev && nxdup

nxdup:
	tmux new -A -s xdev && tmux send -t xdev "docker compose --env-file .env -p xdev_p312 -f containers/fotoantara/xdev.yml up" ENTER

nxdev: nxdup

xdupr:
	docker compose --env-file .env -p xdev_p312 -f containers/fotoantara/xdev.yml up --build

xdb:
	docker compose --env-file .env -p xdev_p312 -f containers/fotoantara/xdev.yml up --build

xddown:
	docker compose --env-file .env -p xdev_p312 -f containers/fotoantara/xdev.yml down

nw:
	docker network create ${NETWORK}

xteup:
	docker compose --env-file .env -f containers/fotoantara/xtree.yaml up 
xtedown:
	docker compose --env-file .env -f containers/fotoantara/xtree.yaml down 
xte:
	docker exec -it tree_flask bash

scup:
	docker compose --env-file .env -p xscraping -f containers/fotoantara/xscraping.yaml up 
scdown:
	docker compose --env-file .env -p xscraping -f containers/fotoantara/xscraping.yaml down 

sc:
	docker compose --env-file .env -p xscraping -f containers/fotoantara/xscraping.yaml exec scraping_flask bash

xup:
	docker compose --env-file .env -p xflask_p11 -f containers/fotoantara/xflask.yml up 
	
xupr:
	docker compose --env-file .env -p xflask_p11 -f containers/fotoantara/xflask.yml up --build

xupv:
	docker compose --env-file .env -f containers/fotoantara/xflask.yml up xflask:v1

xupr2:
	@echo "\033[1;36m🚀 Building and starting xflask...\033[0m"
	DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 \
	docker compose \
		-p xflask_p11 \
		-f containers/fotoantara/xflask.yml \
		build
	DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 \
	docker compose \
		-p xflask_p11 \
		-f containers/fotoantara/xflask.yml \
		up

xb:
	docker compose --env-file .env -p xflask_p11 -f containers/fotoantara/xflask.yml --build

xdown:
	docker compose --env-file .env -p xflask_p11 -f containers/fotoantara/xflask.yml down

xdownk:
	docker compose --env-file .env -p xflask_p11 -f containers/fotoantara/xflask.yml down
	tmux kill-session -t xflask
	
xupf:
	tmux new -A -s xflask && tmux send -t xflask "python3 -c \"docker compose --env-file .env -f containers/fotoantara/xflask.yml up\"" ENTER

rsc: scdown
	@chmod +x ./containers/fotoantara/sc.sh
	@tmux kill-session -t scraping 2>/dev/null || true
	@/bin/bash ./containers/fotoantara/sc.sh

rxflask: xdown
	tmux kill-session -t xflask && chmod +x ./containers/fotoantara/xflask.sh && . ./containers/fotoantara/xflask.sh

rxtest:
	tmux kill-session -t xtest && chmod +x ./containers/fotoantara/xtest.sh && . ./containers/fotoantara/xtest.sh

rxt: xtdown
	@chmod +x ./containers/fotoantara/xt.sh
	@tmux kill-session -t xt 2>/dev/null || true
	@/bin/bash ./containers/fotoantara/xt.sh

nvpn:
	. vpnwsl2.sh
	tmux a -t vpnwsl

rvpn:
	tmux kill-session -t vpnwsl && /home/${USER}/flask/vpnwsl2.sh

vpn:
	cd ~/wsl-vpn && sudo ./wsl-vpnkit-start.sh

rovpn:
	tmux kill-session -t ovpn && /home/${USER}/flask/ovpn.sh
# sudo openvpn --config /etc/openvpn/config.conf

selv:
	python3 -c "import selenium; print(selenium.__version__)" 

bk:
	. razan/backupfile.sh
z:
	pip freeze > /home/${USER}/flask/notebook/data/$m.txt

zz:
	pip freeze > /home/${USER}/flask/data/backup/reqco_detail.txt
	obsutil cp /home/${USER}/flask/data/backup/reqco_detail.txt obs://data-team/modultxt/reqco_detail.txt

fz:
	pip freeze > /home/ubuntu/flask/data/agus/data/req_apps2.txt
	./tosutil cp data/agus/data/req_apps2.txt tos://data-team/modultxt/req_apps2.txt --acl public-read

ft:
	./tosutil cp data/agus/data/req_apps2.txt tos://data-team/modultxt/req_apps2.txt --acl public-read

fr:
	./tosutil cp razan/reqco.txt tos://data-team/modultxt/reqco.txt --acl public-read

ck:
	python -m pip check

tvpn:
	cd /home/${USER}/flask/ && python3 -c "from razan import cfg; conn = cfg.lcd(); conn.cursor(); conn.close()" 

apx:
	cd /home/${USER}/flask/ && python3 -c "from app.auto_content import automated_jagung as act; act.ac_jisdor()" 

acjisdor: apx

ihsg_hist:
	cd /home/${USER}/flask/ && python -c "from app.scraping import update_idx as idx; idx._update_ihsg_idx();" 

scihsg:
	cd /home/${USER}/flask/ && python -c "from app.scraping import update_idx as idx; idx.update_ihsg_hist();" 

seriesu:
	cd /home/${USER}/flask/ && python -c "from razan import rzn; from importlib import reload as rl; rzn.series_update_belum();" 

ogre:
	cd /home/${USER}/flask/ && python -c "from importlib import reload as rl; from razan import selenium_cms_get_ogimage as og; rl(og); og.edit_ogimage_en(recreate=True);" 

ognew:
	cd /home/${USER}/flask/ && python -c "from importlib import reload as rl; from razan import selenium_cms_get_ogimage as og; rl(og); og.edit_ogimage_en(recreate=False);" 

oggg:
	cd /home/${USER}/flask/ && python -c "from importlib import reload as rl; from razan import selenium_cms_get_ogimage as og; rl(og); og.edit_ogimage_en_gagal();" 

pipu:
	python3 -m pip install --upgrade pip --user

rmysql: mysql-restart
# sudo pip3 install selenium
##'4.1.1'

# rm:
# 	rm /path/to/directory/*
# rm df_temp*.pkl
dikti:
	python -c "from app.scraping import scraping_pddikti_api as pddikti; from importlib import reload as rl; rl(pddikti); pddikti.get_gage_dikti(to_db=True, not_exist=True, test=False);"
	
cbash: grid-chrome-bash

szapps:
	sudo du -shc /var/cache/apt
	sudo journalctl --disk-usage
	sudo du -shc ~/.cache/thumbnails
	dpkg-query -W -f='${Installed-Size;8}  ${Package}\n' | sort -n

# sz:
# 	du -sh * | sort -h

cc:
	rm -rf ~/.local/share/Trash/*
	find data/logs/ -type f \( -name "*zip" -o -name "*tar" -o -name "*gz" -o -name "*log" \) -size +1M -exec rm {} +
	sudo journalctl --vacuum-time=7d
	sudo rm -rf ~/.cache/thumbnails/*
	sudo find data/cache -type f -regex '.*\.csv' -delete
	sudo journalctl --vacuum-size=500M
	sudo apt-get autoremove
	sudo apt-get clean
	sudo apt-get autoclean
# 	find /home/${USER}/flask/.wdm -type f -delete
# 	find /home/${USER}/flask/data/cache -type f -delete
# remove with all subdirectory
	find /home/${USER}/flask/.wdm -mindepth 1 -delete
	find /home/${USER}/flask/data/cache -mindepth 1 -delete


# 	sudo rm -rf ~/.wdm/*
# 	sudo rm -rf /home/${USER}/flask/.wdm/*
# 	sudo rm -rf /home/${USER}/flask/data/cache/*

ccbash: cbash
	sudo find /home/seluser/Downloads -type f -regex ".*\.zip$\" -delete

# sudo chwon - R ${USER} && rm -rf 

ihsg:
	tmux new-session -d -s ihsg
	tmux send-keys -t ihsg 'python3 -c "from app.scraping import update_idx as idx; idx.update_ihsg_hist();"' Enter
	tmux attach-session -t ihsg

idx:
	tmux new-session -d -s idxs
	tmux send-keys -t idxs 'python3 -c "from app.scraping import update_histori_investing as idx; idx.belum_update(updatedata=True);"' Enter
	tmux attach-session -t idxs

shm:
	tmux new-session -d -s shm
	tmux send-keys -t shm 'python3 -c "from app import job; job.run_scsaham();"' Enter
	tmux attach-session -t shm

iskat:
	docker exec -it ${PCDOCKER} bash -c " \
		tmux kill-session -t iskat 2>/dev/null || true; \
		tmux new-session -d -s iskat 'bash'; \
		tmux send-keys -t iskat 'python3 -c \"from razan import rzn; rzn.is_kategori()\"' Enter; \
		sleep 1; \
		tmux attach-session -t iskat \
	"

is_series: iskat

shm_host:
	docker exec -it ${PCDOCKER} bash -c " \
		tmux kill-session -t shm 2>/dev/null || true; \
		tmux new-session -d -s shm 'bash'; \
		tmux send-keys -t shm 'python3 -c \"from app import job; job.run_scsaham()\"' Enter; \
		sleep 1; \
		tmux attach-session -t shm \
	"

shm_bg:
	docker exec ${PCDOCKER} bash -c " \
	tmux kill-session -t shm 2>/dev/null || true \
	tmux new-session -d -s shm 'python3 -c \"from app import job; job.run_scsaham()\"'"
	@echo "✅ Job berjalan di tmux session 'shm' di dalam container ${PCDOCKER}"

cfoto:
	python3 -c "from razan import rzn; rzn.clear_foto();"

mem:
	. /home/${USER}/flask/memusage.sh
## ===================== Maintained By: irfan-fadhlurrahman ==========================
# General

backup-autostart:
	cp .env ./app/shell_script/.env
	chmod +x app/shell_script/backup.sh && . ./app/shell_script/backup.sh

backup-attach:
	tmux a -t backup

backup-kill:
	tmux kill-session -t backup

backup-restart: backup-kill backup-autostart backup-attach

daily-data-series:
	python3 app/update_data_series.py daily

daily-data-series-freq:
	python3 app/update_data_series.py daily '$(MESSAGE)'

update-data-series:
	python3 app/update_data_series.py non_daily

show-file-dir:
	ls -al

commit-to-github:
	echo '$(MESSAGE)'
	git add .
	git commit -m '$(MESSAGE)'
	git pull origin main
	git push origin main

docker-stats-json:
	docker stats --format "{\"name\":\"{{ .Name }}\",\n\"memory\":{\"raw\":\"{{ .MemUsage }}\",\"percent\":\"{{ .MemPerc }}\"},\n\"cpu\":\"{{ .CPUPerc }}\"}\n"

remove-docker-cache:
	echo "This command will make next image building slower"
	docker builder prune -a
	
update-image:
	docker compose build

spin-up:
	docker compose --env-file .env up

spin-down:
	docker compose down --remove-orphans

kill-session:
	docker compose down --remove-orphans
	tmux kill-session -t web_scraping

fix-file-permissions:
	sudo chown -R $${USER} .

fix-docker-permission:
	sudo chmod 666 /var/run/docker.sock

auto-pull:
	git add .
	git commit -m "auto pull to update scripts"
	git pull ${gittoken}

auto-push:
	git add .
	git commit -m "auto pull to update"
	git pull origin main
	git push origin main

install-docker:
	chmod +x ./init.sh && . ./init.sh
	docker network create my-network

update-google-token:
	# Only works on huawei server
	python3 quickstart.py

# Docker Compose
up:
	docker compose --env-file .env -f setup/docker-compose.yml up --build

down:
	docker compose down --remove-orphans

rebuild: down up
	docker compose down --remove-orphans

shell:
	docker compose -f docker-compose-apscheduler.yml --env-file .env exec apscheduler bash

# Continuous Integration
format:
	docker exec apscheduler python -m black -S --line-length 90 .

isort:
	docker exec apscheduler isort .

pytest:
	docker exec apscheduler pytest /opt/code/tests -s --disable-warnings

pytest-common:
	pytest /opt/code/tests/units/test_common.py -k test_get_driver

type:
	docker exec apscheduler mypy --ignore-missing-imports /opt/code

lint: 
	docker exec apscheduler flake8 /opt/code 

ci: isort format type lint pytest

# MySQL
mysql-bash:
	cd ./containers/flask-mysql && docker compose -f docker-compose.dev.yml exec mysqldb bash

mysql-up:
	cp .env ./containers/flask-mysql
	cd ./containers/flask-mysql && docker compose --env-file .env -f docker-compose.dev.yml up -d --build

mysql-down:
	cp .env ./containers/flask-mysql
	cd ./containers/flask-mysql && docker compose --env-file .env -f docker-compose.dev.yml down --remove-orphans

mysql-autostart:
	cp .env ./containers/flask-mysql
	chmod +x containers/flask-mysql/autostart_mysql.sh && . ./containers/flask-mysql/autostart_mysql.sh

mysql-attach:
	tmux a -t mysql-databoks

mysql-kill:
	tmux kill-session -t mysql-databoks

mysql-restart: mysql-down mysql-kill mysql-autostart mysql-attach

mysql-rebuild: mysql-down mysql-kill mysql-up mysql-down mysql-autostart mysql-attach

# CDC Debezium
kafka-bash:
	cd ./containers/debezium && docker compose -f kafka-debezium.yml exec kafka bash

debezium-bash:
	cd ./containers/debezium && docker compose -f kafka-debezium.yml exec connect bash

cdc-data-lite-consumer:
	cd ./containers/debezium && \
	docker compose --env-file .env -f kafka-debezium.yml exec kafka /kafka/bin/kafka-console-consumer.sh \
		--bootstrap-server kafka:9092 \
		--from-beginning \
		--topic dbserver1.cdc.data_lite \
		> log/message.json

mysql-cdc-up:
	cd ./containers/debezium && docker compose -f kraft-debezium.yml up mysql

cdc-up:
	cd ./containers/debezium && docker compose -f kafka-debezium.yml up --build

cdc-down:
	cd ./containers/debezium && docker compose -f kafka-debezium.yml down --remove-orphans

cdc-autostart:
	chmod +x ./containers/debezium/autostart.sh && . ./containers/debezium/autostart.sh

cdc-attach:
	tmux a -t debezium

cdc-kill:
	tmux kill-session -t debezium

cdc-restart: cdc-kill cdc-autostart cdc-attach

cdc-rebuild: cdc-down cdc-kill cdc-up cdc-down cdc-autostart cdc-attach

# Selenium Grid
grid-rm-perfctl:
	docker compose --env-file .env -f containers/selenium_grid/docker-compose-grid.yml exec chrome-v1 bash -c 'ls -al /home/seluser/.config; rm -rf /home/seluser/.config/cron/perfcc'

grid-chrome-bash:
	docker compose --env-file .env -f containers/selenium_grid/docker-compose-grid.yml exec chrome-v1 bash

grid-up:
	docker compose --env-file .env -f containers/selenium_grid/docker-compose-grid.yml up

grid-down:
	docker compose --env-file .env -f containers/selenium_grid/docker-compose-grid.yml down --remove-orphans

grid-autostart:
	chmod +x ./containers/selenium_grid/autostart.sh && . ./containers/selenium_grid/autostart.sh

grid-attach:
	tmux a -t selenium_grid

grid-kill:
	tmux kill-session -t selenium_grid

grid-restart: grid-kill grid-autostart grid-attach

grid-rebuild: grid-down grid-kill grid-up grid-down grid-autostart grid-attach

env:
	source /home/${USER}/flask/.venv/bin/activate

# APScheduler
apscheduler-up:
	docker compose -f docker-compose-apscheduler.yml --env-file .env up -d --build

apscheduler-down:
	docker compose -f docker-compose-apscheduler.yml down

apscheduler-autostart:
	chmod +x ./containers/apscheduler/autostart.sh && . ./containers/apscheduler/autostart.sh

apscheduler-attach:
	tmux a -t apscheduler

apscheduler-kill:
	tmux kill-session -t apscheduler

rsch: apscheduler-kill apscheduler-autostart apscheduler-attach

apscheduler-restart: apscheduler-kill apscheduler-autostart apscheduler-attach

apscheduler-rebuild: apscheduler-down apscheduler-kill apscheduler-up apscheduler-down apscheduler-autostart apscheduler-attach

# Jupyter
jupyter-bash:
	docker compose --env-file .env -f docker-compose-jupyter.yml exec jupyter bash

jupyter-up:
	docker compose -f docker-compose-jupyter.yml --env-file .env up -d --build

jupyter-down:
	docker compose -f docker-compose-jupyter.yml down

jupyter-autostart:
	chmod +x ./containers/jupyter/autostart.sh && . ./containers/jupyter/autostart.sh

jupyter-attach:
	tmux a -t jupyter

jupyter-kill:
	tmux kill-session -t jupyter

jupyter-restart: jupyter-kill jupyter-autostart jupyter-attach

jupyter-rebuild: jupyter-down jupyter-kill jupyter-up jupyter-down jupyter-autostart jupyter-attach

# Chroma
chroma-bash:
	cd ./containers/fastapi-chroma && docker compose -f docker-compose-chroma.yml exec semantic-search bash

chroma-up:
	cd ./containers/fastapi-chroma && docker compose -f docker-compose-chroma.yml up -d --build

chroma-down:
	cd ./containers/fastapi-chroma && docker compose -f docker-compose-chroma.yml down

chroma-autostart:
	chmod +x ./containers/fastapi-chroma/autostart.sh && . ./containers/fastapi-chroma/autostart.sh

chroma-attach:
	tmux a -t chroma

chroma-kill:
	tmux kill-session -t chroma

chroma-restart: chroma-kill chroma-autostart chroma-attach

chroma-rebuild: chroma-down chroma-kill chroma-up chroma-down chroma-autostart chroma-attach

# minio
minio-bash:
	cp .env ./containers/minio
	cd ./containers/minio && docker compose --env-file .env -f docker-compose-minio.yml exec minio bash

minio-up:
	cp .env ./containers/minio
	cd ./containers/minio && docker compose --env-file .env -f docker-compose-minio.yml up -d --build

minio-down:
	cd ./containers/minio && docker compose -f docker-compose-minio.yml down

minio-autostart:
	chmod +x ./containers/minio/autostart.sh && . ./containers/minio/autostart.sh

minio-attach:
	tmux a -t minio

minio-kill:
	tmux kill-session -t minio

minio-restart: minio-kill minio-autostart minio-attach

minio-rebuild: minio-down minio-kill minio-up minio-down minio-autostart minio-attach

# mongodb
mongodb-bash:
	cp .env ./containers/mongodb
	cd ./containers/mongodb && docker compose --env-file .env -f docker-compose-mongodb.yml exec mongodb bash

mongodb-up:
	cp .env ./containers/mongodb
	cd ./containers/mongodb && docker compose --env-file .env -f docker-compose-mongodb.yml up --build

mongodb-down:
	cd ./containers/mongodb && docker compose -f docker-compose-mongodb.yml down

mongodb-autostart:
	chmod +x ./containers/mongodb/autostart.sh && . ./containers/mongodb/autostart.sh

mongodb-attach:
	tmux a -t mongodb

mongodb-kill:
	tmux kill-session -t mongodb

mongodb-restart: mongodb-kill mongodb-autostart mongodb-attach

mongodb-rebuild: mongodb-down mongodb-kill mongodb-up mongodb-down mongodb-autostart mongodb-attach

# sentiment
sentiment-bash:
	cp .env ./containers/sentiment_analysis
	cd ./containers/sentiment_analysis && docker compose --env-file .env -f sentiment.yaml exec sentiment bash

sentiment-up:
	cp .env ./containers/sentiment_analysis
	cd ./containers/sentiment_analysis && docker compose --env-file .env -f sentiment.yaml up --build

sentiment-down:
	cd ./containers/sentiment_analysis && docker compose -f sentiment.yaml down

sentiment-autostart:
	chmod +x ./containers/sentiment_analysis/autostart.sh && . ./containers/sentiment_analysis/autostart.sh

sentiment-attach:
	tmux a -t sentiment

sentiment-kill:
	tmux kill-session -t sentiment

sentiment-restart: sentiment-kill sentiment-autostart sentiment-attach

sentiment-rebuild: sentiment-down sentiment-kill sentiment-up sentiment-down sentiment-autostart sentiment-attach

# Production
production-bash:
	docker compose --env-file .env -f containers/python3.12/1_development.yaml exec python3-12-dev bash

production-build:
	cp .env ./containers/python3.12
	docker compose --env-file .env -f containers/python3.12/1_development.yaml build

production-up:
	docker compose --env-file .env -f containers/python3.12/1_development.yaml up

production-down:
	docker compose --env-file .env -f containers/python3.12/1_development.yaml down

production-remove-orphans:
	docker compose --env-file .env -f containers/python3.12/1_development.yaml down --remove-orphans

production-autostart: 
	chmod +x ./containers/python3.12/1_autostart_dev.sh && . ./containers/python3.12/1_autostart_dev.sh

production-attach:
	tmux a -t production

production-kill:
	tmux kill-session -t production

production-restart: production-kill production-autostart production-attach

production-rebuild: production-down production-kill production-build production-autostart production-attach

# Development
development-bash:
	docker compose --env-file .env -f containers/apscheduler-python3.11/development.yml exec apscheduler-dev bash

development-build:
	cp .env ./containers/apscheduler-python3.11
	docker compose --env-file .env -f containers/apscheduler-python3.11/development.yml build

development-up:
	docker compose --env-file .env -f containers/apscheduler-python3.11/development.yml up

development-down:
	docker compose --env-file .env -f containers/apscheduler-python3.11/development.yml down

development-remove-orphans:
	docker compose --env-file .env -f containers/apscheduler-python3.11/development.yml down --remove-orphans

development-autostart: 
	chmod +x ./containers/apscheduler-python3.11/autostart_dev.sh && . ./containers/apscheduler-python3.11/autostart_dev.sh

development-attach:
	tmux a -t development

development-kill:
	tmux kill-session -t development

development-restart: development-kill development-autostart development-attach

development-rebuild: development-down development-kill development-build development-autostart development-attach

# Metabase
metabase-bash:
	cd ./containers/metabase && docker compose --env-file .env -f metabase.yml exec metabase bash

metabase-build:
	cp .env ./containers/metabase
	cd ./containers/metabase && docker compose --env-file .env -f metabase.yml build

metabase-up:
	cd ./containers/metabase && docker compose --env-file .env -f metabase.yml up

metabase-down:
	cd ./containers/metabase && docker compose --env-file .env -f metabase.yml down

metabase-remove-orphans:
	cd ./containers/metabase && docker compose --env-file .env -f metabase.yml down --remove-orphans

metabase-autostart: 
	chmod +x ./containers/metabase/autostart.sh && . ./containers/metabase/autostart.sh

metabase-attach:
	tmux a -t metabase

metabase-kill:
	tmux kill-session -t metabase

metabase-restart: metabase-kill metabase-autostart metabase-attach

metabase-rebuild: metabase-down metabase-kill metabase-build metabase-autostart metabase-attach


# Backup (run on MySQL bash)
mysql-dump-no-data:
	mysqldump -u root -p --no-data databoks_production > /var/lib/mysql/20240118_schema_databoks_production.sql
	mysqldump -u root -p --no-data databoks_development > /var/lib/mysql/20240118_schema_databoks_development.sql

mysql-dump-database:
	mysqldump -u root -p --databases databoks_production > /var/lib/mysql/databoks_production.sql
	mysqldump -u root -p databoks_production --default-character-set=utf8 > /var/lib/mysql/database.sql
	mysql -uroot -p$MYSQL_PASSWORD databoks_production < /var/lib/mysql/backup.sql
	pgloader mysql://root:d4taBokS@192.168.50.250:3306/databoks_production pgsql://dbadmin:"Katadata&Grava1928"@110.239.65.168:8000/databoks_production

restore-database:
	mysql -u root -p databoks_production < /db/20231101_databoks_production_db.sql
	mysql -u root -p databoks_development < /db/20231101_databoks_development.sql

restarter-vm-database:
	tmux kill-session -t restarter; . app/shell_script/restart_container.sh vm-database; tmux a -t restarter

restarter-vm-scraping:
	tmux kill-session -t restarter; . app/shell_script/restart_container.sh vm-scraping; tmux a -t restarter

restarter-vm-huawei:
	tmux kill-session -t restarter; . app/shell_script/restart_container.sh vm-huawei; tmux a -t restarter

# Temporary Jupyter
jupyter-temp:
	apt install curl make -y; pip install jupyter jupyterlab ipywidgets; jupyter lab --no-browser --ip=0.0.0.0 --port=8988 --allow-root --NotebookApp.token=${JUPYTER_TOKEN} --NotebookApp.disable_check_xsrf=True

jupyter-local:
	# http://127.0.0.1:8988/lab?token=123456
	pip install jupyter jupyterlab ipywidgets; jupyter lab --no-browser --ip=0.0.0.0 --port=8988 --NotebookApp.token=123456

jupyter-temp-311:
	apt install curl make -y; pip install jupyter jupyterlab ipywidgets; jupyter lab --no-browser --ip=0.0.0.0 --port=8878 --allow-root --NotebookApp.token=${JUPYTER_TOKEN} --NotebookApp.disable_check_xsrf=True

jupyter-wsl:
	chmod +x ./jupyter_autostart.sh && . ./jupyter_autostart.sh; tmux a -t jupyter

zip-flask:
	cd ; time sudo zip -r -q flask.zip flask

# Cron (MUST CHANGE "/home/databoks/web_scrapping" based on your directory)
# @reboot . /home/databoks/web_scrapping/containers/apscheduler/autostart.sh; sleep 10
# @reboot . /home/databoks/web_scrapping/containers/apscheduler-python3.11/autostart_dev.sh; sleep 10
# @reboot . /home/databoks/web_scrapping/containers/jupyter/autostart.sh; sleep 10
# @reboot . /home/databoks/web_scrapping/containers/selenium_grid/autostart.sh
# @reboot . /home/databoks/web_scrapping/containers/fastapi-chroma/autostart.sh
# @reboot . /home/databoks/web_scrapping/containers/minio/autostart.sh
# @reboot . /home/databoks/web_scrapping/containers/mongodb/autostart.sh