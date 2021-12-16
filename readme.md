## 看图识片工具人

根据截图搜寻到本地数据库内与截图最相似的视频



### 典型用法介绍

#### 首先使用 preprocessing 脚本生成某一文件夹内视频文件的数据库
例：
    
    python preprocessing videos/handuty/ --target_dir dataset/ --recursive
将递归地处理 videos/handuty 文件夹及其子文件夹中的视频，并将在 dataset 文件夹内生成数据库


    python preprocessing.py  <videos_dir> --target_dir <target_dir> [--recursive] [--continue_on] [--width width] [-height height]

    --target_dir 指明了生成的数据库存放位置

    --recursive 标志了是否会递归的处理视频文件夹，没有此标志则默认仅处理视频文件夹内的第一层视频文件

    --continue_on 标志了是否以之前的数据库为基础继续生成数据，没有此标志则会覆盖数据库存放位置的原数据

    --width 与 --height 指明了生成的数据库所使用的每帧图像大小，一般不需要改变

这些参数可通过 python preprocessing --help 来查看

#### 之后使用 find_my 脚本在数据库中搜寻某一截图

例：
    
    python find_vid.py test.jpg dataset/ 

将在 dataset 文件夹内的数据库中搜寻 test.jpg 图像所属的视频

    python find_vid.py <picture> <dataset> --multi_datasets

    picture 为要搜寻的截图所在位置

    dataset 为数据库所在位置

    --multi_datasets 指明了 dataset 目录下是否有多个数据库。若要使用多个数据库进行检索，则应当将所有数据库文件夹组织如下：

    --dataset_total
        |
    ----dataset1
        |
    ----dataset2
    
# 需要的 python 库
    cv2, numpy

# 注意：
很多视频文件可能由于年代久远以及在不同软件中往复辗转，编码会出现问题（尤其尤其尤其是 wmv 文件），因此无法生成正常的数据库，目前没有好的解决办法

# 已生成的数据库
可直接下载解压供 find_vid.py 脚本使用

spanking movie jp: https://mega.nz/file/cJgS2CRJ#d9oReFbNjdgrz99eFEJFPAv8cBRD-dbc3dDUZs2QNqo
    

汉责: https://mega.nz/file/0FgzDShJ#WG-vkbpnDDdc7XPqYALQNNV4DxUGL_OW6QC_6LKj5NM
