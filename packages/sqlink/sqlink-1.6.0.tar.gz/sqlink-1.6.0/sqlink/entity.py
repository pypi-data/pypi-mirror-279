# -*- coding: utf-8 -*-
import copy
from dataclasses import dataclass, is_dataclass
from typing import Union

# ====================================================================================================================
# 模块常量
DEFINE_TYPE_IGNORE = "ignore"
DEFINE_TYPE_PRIMARY_KEY = "primary_key"
DEFINE_TYPE_AUTO_PRIMARY_KEY = "auto_primary_key"
DEFINE_TYPE_NOT_NULL = "not_null"
DEFINE_TYPE_UNIQUE = "unique"
DEFINE_TYPE_FOREIGN_KEY = "foreign_key"
DEFINE_TYPE_DEFAULT = "default"
DEFINE_TYPE_CHECK = "check"
DEFINE_TYPE_COMMENT = "comment"
DEFINE_TYPE_DATATYPE = "datatype"

ENTITY_INIT = "__entity_init__"
FOREIGN_KEY_PLACEHOLDER = "_"


@dataclass
class _Define:
    """内部维护的约束类，存储实际约束"""
    type: str
    value: str = ""

    def __hash__(self):
        return hash(self.value)


# ====================================================================================================================
def Entity(check_type: bool = False):
    """数据类dataclass的装饰器。

    在定义dataclass时，同时将约束条件和默认值赋予类属性。
    通过改造原生dataclass的init方法和getattribute方法，实现sql建表时约束条件的解析，以及正常使用被装饰dataclass时属性值的获取。

    Args:
        check_type(bool): 若传入True，实例化数据类时会检查属性值类型和注释的类型是否一致，不一致将触发类型错误。

    Example1:
        @Entity
        @dataclass
        class Student:  # 类名即表名，不区分大小写
            name: str  # 字段名以及字段类型
            score: float = 100

    Example2:
        @Entity(check_type=True)  # 启用类型检查
        @dataclass
        class Student:
            name: str
            score: float = 100.0
            # Example1中的score属性虽然注释为float，实际默认值为int，但仍然可以正常工作（由于python和sqlite都是宽松的类型约束）。

    !Note:
        在实用角度上@dataclass应该合并到@Entity内部，这样定义数据类时只需要使用一个装饰器，并且不需要使用者关心什么是dataclass，
        但经过测试发现，如果不显式的使用@dataclass装饰器，在实例化数据类时Pycharm将无法给出代码提示，这是不可忍受的。
        并且只有Pycharm2020及之前的版本可以正确给出代码提示，高于2020版存在代码提示的bug，详见:
        https://intellij-support.jetbrains.com/hc/en-us/community/posts/4421575751442-Code-Completion-doesn-t-work-for-class-functions-decorated-with-decorators-that-return-inner-functions

    """

    def decorator(cls):
        if not is_dataclass(cls):
            cls = dataclass(cls)
        orig_get_attr = cls.__getattribute__
        orig_init = cls.__init__

        def get_attr(self, name):
            """重写被装饰dataclass的取值方法"""
            # 只有访问定义的属性时才进一步处理
            orig_value = orig_get_attr(self, name)
            if name in set(attr_name for attr_name, attr_type in cls.__annotations__.items()):
                return _parse_attr_value(orig_value)
            # 访问其他属性则返回原始值
            return orig_value

        def init_and_check_type(self, *args, **kwargs):
            """重写被装饰dataclass的初始化方法"""
            orig_init(self, *args, **kwargs)
            for attr_name, attr_type in cls.__annotations__.items():
                # 排除忽略属性
                orig_value = getattr(cls, attr_name, None)
                if any(define.type == DEFINE_TYPE_IGNORE for define in _parse_defines(orig_value)):
                    continue
                # 再检查属性值的类型与类型注解是否一致
                attr_value = get_attr(self, attr_name)
                # 不检查默认值为None的属性
                if attr_value is None:
                    continue
                elif not isinstance(attr_value, attr_type):
                    raise TypeError(
                        f"实例化'{cls.__name__}'类时,"
                        f"'{attr_name}'属性的类型应该是 '{attr_type.__name__}' ,"
                        f"但得到的是 '{type(attr_value).__name__}'")

        # 由于无参装饰器的特性，在无参使用该装饰器时，check_type的值被覆盖为cls，因此必须显式的与True进行判断
        if check_type == True:  # noqa
            cls.__init__ = init_and_check_type
        setattr(cls, ENTITY_INIT, orig_init)
        cls.__getattribute__ = get_attr
        return cls

    # 无参使用该装饰器时
    if callable(check_type):
        return decorator(cls=check_type)  # noqa

    return decorator


def is_entity(obj) -> bool:
    """判断该对象是否是entity数据类"""
    return hasattr(obj, ENTITY_INIT)


class Define:
    """对外开放的各种字段定义。

    Example:
        @Entity
        @dataclass
        class Student:
            name: str  # 可以不使用约束
            score: float = 100  # 可以只赋予默认值
            address: str = 'HIT', Define.not_null  # 同时使用默认值和约束，需要以逗号分隔开，顺序任意
            student_id: int = Define.auto_primary_key, Define.not_null  # 同时使用多条约束，需要以逗号分隔开

    !Note:
        建议导入Define类时使用别名，可以有效简化存在大量约束的使用场景。

        Example:
            from sqlink import Define as d

            @Entity
            @dataclass
            class Student:
                name: str
                score: float = 100
                address: str = 'HIT', d.not_null
                student_id: int = d.auto_primary_key, d.not_null

    """

    # =================================================================================================================
    # 1.可直接使用的约束
    # 主键
    primary_key = _Define(value="PRIMARY KEY",
                          type=DEFINE_TYPE_PRIMARY_KEY)
    # 自增主键
    auto_primary_key = _Define(value="PRIMARY KEY",
                               type=DEFINE_TYPE_AUTO_PRIMARY_KEY)
    # 非空约束
    not_null = _Define(value="NOT NULL",
                       type=DEFINE_TYPE_NOT_NULL)
    # 唯一性约束
    unique = _Define(value="UNIQUE",
                     type=DEFINE_TYPE_UNIQUE)
    # 针对外键的约束
    no_action = 'NO ACTION'
    cascade = 'CASCADE'
    set_null = 'SET NULL'
    restrict = 'RESTRICT'
    set_default = 'SET DEFAULT'

    # 非sql的特殊约束
    # 用于建表时忽略某字段/属性
    ignore = _Define(type=DEFINE_TYPE_IGNORE)

    # =================================================================================================================
    # 2.需要外部传值的约束
    @staticmethod
    def default(default_value: Union[int, str, float, bytes, bool, type(None)], /):
        """默认值约束

        Args:
            default_value: 该字段在sql中的默认值，与定义数据类时使用默认值作用类似。

        Example:
            @Entity
            @dataclass
            class Student:
                name: str
                score1: float = 100
                score2: float = Define.default(100)  # 与score1作用类似
                student_id: int = Define.auto_primary_key

        """
        return _Define(value=f'DEFAULT {default_value}',
                       type=DEFINE_TYPE_DEFAULT)

    @staticmethod
    def check(check_condition: str):
        """条件约束

        Args:
            check_condition: 具体条件

        Example:
            @Entity
            @dataclass
            class Student:
                name: str
                score: float = Define.check('score > 60')  # 需要填写该字段的字符形式名称
                student_id: int = Define.auto_primary_key

        """
        return _Define(value=f'CHECK({check_condition})',
                       type=DEFINE_TYPE_CHECK)

    # @staticmethod
    # def foreign_key(parent_entity, parent_field, delete_link=None, update_link=None):
    #     """外键约束
    #
    #     Args:
    #         parent_entity: 外键所在的数据类（父表）
    #         parent_field: 外键对应的数据类属性
    #         delete_link: 级联删除方式
    #         update_link: 级联更新方式
    #
    #     Example:
    #         @Entity
    #         @dataclass
    #         class Student:  # 父表
    #             name: str = Define.not_null
    #             student_id: int = Define.auto_primary_key
    #
    #         @Entity
    #         @dataclass
    #         class Score:  # 子表
    #             score: float
    #             score_id: int = Define.auto_primary_key
    #             # 对student_id字段设置外键关联
    #             student_id: int = Define.foreign_key(entity=Student,
    #                                                      field='student_id',
    #                                                      delete_link=Define.cascade,
    #                                                      update_link=Define.cascade)
    #
    #     """
    #     parent_entity = parent_entity.__name__.lower()
    #     parent_field = parent_field.lower()
    #     if delete_link is None and update_link is None:
    #         foreign_key = f"FOREIGN KEY ({FOREIGN_KEY_PLACEHOLDER}) " \
    #                       f"REFERENCES {parent_entity}({parent_field})"
    #
    #     elif delete_link is not None and update_link is None:
    #         foreign_key = f"FOREIGN KEY ({FOREIGN_KEY_PLACEHOLDER}) " \
    #                       f"REFERENCES {parent_entity}({parent_field}) ON DELETE {delete_link}"
    #
    #     elif delete_link is None and update_link is not None:
    #         foreign_key = f"FOREIGN KEY ({FOREIGN_KEY_PLACEHOLDER}) " \
    #                       f"REFERENCES {parent_entity}({parent_field}) ON UPDATE {update_link}"
    #
    #     elif delete_link is not None and update_link is not None:
    #         foreign_key = f"FOREIGN KEY ({FOREIGN_KEY_PLACEHOLDER}) " \
    #                       f"REFERENCES {parent_entity}({parent_field}) " \
    #                       f"ON DELETE {delete_link} ON UPDATE {update_link} "
    #     else:
    #         raise TypeError(
    #             f"错误使用了外键约束")
    #
    #     return _Define(value=foreign_key,
    #                        type=DEFINE_TYPE_FOREIGN_KEY)

    @staticmethod
    def comment(comment: str, /):
        """字段注释

        Args:
            comment: 具体注释。注意，在sqlite中只能通过DDL(Data Definition Language)查看。

        Example:
            @Entity
            @dataclass
            class Student:
                name: str = Define.comment('学生姓名')
                student_id: int = Define.auto_primary_key, Define.comment('学生id')

        """
        return _Define(value=comment,
                       type=DEFINE_TYPE_COMMENT)

    @staticmethod
    def datatype(data_type: str, /):
        return _Define(value=data_type,
                       type=DEFINE_TYPE_DATATYPE)


# ====================================================================================================================
# 模块方法
def _parse_defines(attr_value) -> list[_Define]:
    """从属性原始值中解析出定义。"""
    # 无约束
    defines = []
    # 是单约束
    if isinstance(attr_value, _Define):
        defines = [copy.copy(attr_value)]
    # 包含多约束
    elif isinstance(attr_value, tuple):
        for item in attr_value:
            if not isinstance(item, _Define):
                continue

            # 自动跳过重复约束
            if item not in defines:
                defines.append(copy.copy(item))

    return defines


def _parse_attr_value(attr_value) -> Union[int, str, float, bytes, bool, type(None)]:
    """从属性原始值中过滤约束条件，解析出真正的属性值。并不负责检查值是否匹配类型。"""
    # 单个约束
    if isinstance(attr_value, _Define):
        return None
    # 多约束
    elif isinstance(attr_value, tuple):
        parsed_value = []

        for item in attr_value:
            if not isinstance(item, _Define):
                parsed_value.append(item)

        # 仅多个约束
        if len(parsed_value) == 0:
            return None
        # 包含单个值
        elif len(parsed_value) == 1:
            return parsed_value[0]
        # tuple类型的值
        else:
            return tuple(parsed_value)

    return attr_value
