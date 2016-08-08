from acmnote2.wsgi import *
from authentication.models import MyUser
from problem.models import Problem
from django.contrib.auth.models import User
from util.importproblem import *


def main():
    user = User.objects.get_by_natural_key('xjw')
    my_user = MyUser.objects.get(user=user)

    for pid in range(1000, 1100):
        info = get_hdu_info(pid)
        if info == 'No such problem' or info == 'System error':
            print(str(pid)+":"+info)
            continue
        Problem.objects.update_or_create(
            oj='hdu',
            oj_id=str(pid),
            defaults={'title': info['title'],
                      'time_limit': info['time_limit'],
                      'memory_limit': info['memory_limit'],
                      'description': info['description'],
                      'input_description': info['input_description'],
                      'output_description': info['output_description'],
                      'input': info['input'],
                      'output': info['output'],
                      'create_by': my_user,
                      'hint': '导入功能测试'
                      },
        )
        print(str(pid)+" : success!")

if __name__ == '__main__':
    main()
    print("Done!")
