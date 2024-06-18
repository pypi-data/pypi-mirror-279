"""
WHERE 子句转化器

比较运算符（=）表达式 > 精确查询
IN 表达式 > 多次精确查询
没有 WHERE 语句 > 全匹配查询
比较运算符（>）表达式 > 范围查询
比较运算符（>=）表达式 > 范围查询
比较运算符（<）表达式 > 范围查询
比较运算符（<=）表达式 > 范围查询
LIKE 表达式 > 通配符查询
IS NULL 或 IS NOT NULL 表达式 > 列存在性查询
"""

import tablestore

from metasequoia_sql import node
from otssql.exceptions import NotSupportedError

__all__ = ["convert_where_clause"]


def convert_where_clause(where_clause: node.ASTWhereClause) -> tablestore.Query:
    """将 WHERE 语句转化为 TableStore 的查询条件

    Parameters
    ----------
    where_clause : ASTWhereClause
        WITH 子句的抽象语法树节点

    Returns
    -------
    tablestore.Query
        tablestore 的查询对象
    """
    if where_clause is None:
        return tablestore.MatchAllQuery()
    return change_ast_node_to_tablestore_query(where_clause.condition)


def change_ast_node_to_tablestore_query(ast_node: node.ASTBase) -> tablestore.Query:
    """将抽象语法树节点转化为 TableStore 查询条件

    Parameters
    ----------
    ast_node : ASTBase
        抽象语法树节点

    Returns
    -------
    tablestore.Query
        tablestore 的查询对象
    """
    if isinstance(ast_node, node.ASTOperatorConditionExpression):  # 比较运算符的表达式
        if ast_node.operator.source() == "=":
            if (isinstance(ast_node.before_value, node.ASTColumnNameExpression)
                    and isinstance(ast_node.after_value, node.ASTLiteralExpression)):
                # 字段名 = 字面值
                return tablestore.TermQuery(
                    field_name=ast_node.before_value.column_name,
                    column_value=ast_node.after_value.as_string().strip("'")
                )
            elif (isinstance(ast_node.before_value, node.ASTLiteralExpression)
                  and isinstance(ast_node.after_value, node.ASTColumnNameExpression)):
                # 字面值 = 字段名
                return tablestore.TermQuery(
                    field_name=ast_node.after_value.column_name,
                    column_value=ast_node.before_value.as_string().strip("'")
                )
            raise NotSupportedError("暂不支持的表达式形式（比较运算符前后不是一个字段名、一个字面值）")
        if ast_node.operator.source() == "<":
            if (isinstance(ast_node.before_value, node.ASTColumnNameExpression)
                    and isinstance(ast_node.after_value, node.ASTLiteralExpression)):
                # 字段名 < 字面值
                return tablestore.RangeQuery(
                    field_name=ast_node.before_value.column_name,
                    range_to=ast_node.after_value.as_string().strip("'"),
                    include_upper=False
                )
            elif (isinstance(ast_node.before_value, node.ASTLiteralExpression)
                  and isinstance(ast_node.after_value, node.ASTColumnNameExpression)):
                # 字面值 < 字面名
                return tablestore.RangeQuery(
                    field_name=ast_node.after_value.column_name,
                    range_from=ast_node.before_value.as_string().strip("'"),
                    include_lower=False
                )
            raise NotSupportedError("暂不支持的表达式形式（比较运算符前后不是一个字段名、一个字面值）")
        if ast_node.operator.source() == "<=":
            if (isinstance(ast_node.before_value, node.ASTColumnNameExpression)
                    and isinstance(ast_node.after_value, node.ASTLiteralExpression)):
                # 字段名 <= 字面值
                return tablestore.RangeQuery(
                    field_name=ast_node.before_value.column_name,
                    range_to=ast_node.after_value.as_string().strip("'"),
                    include_upper=True
                )
            elif (isinstance(ast_node.before_value, node.ASTLiteralExpression)
                  and isinstance(ast_node.after_value, node.ASTColumnNameExpression)):
                # 字面值 <= 字段名
                return tablestore.RangeQuery(
                    field_name=ast_node.after_value.column_name,
                    range_from=ast_node.before_value.as_string().strip("'"),
                    include_lower=True
                )
            raise NotSupportedError("暂不支持的表达式形式（比较运算符前后不是一个字段名、一个字面值）")
        if ast_node.operator.source() == ">":
            if (isinstance(ast_node.before_value, node.ASTColumnNameExpression)
                    and isinstance(ast_node.after_value, node.ASTLiteralExpression)):
                # 字段名 > 字面值
                return tablestore.RangeQuery(
                    field_name=ast_node.before_value.column_name,
                    range_from=ast_node.after_value.as_string().strip("'"),
                    include_lower=False
                )
            elif (isinstance(ast_node.before_value, node.ASTLiteralExpression)
                  and isinstance(ast_node.after_value, node.ASTColumnNameExpression)):
                # 字面值 > 字段名
                return tablestore.RangeQuery(
                    field_name=ast_node.after_value.column_name,
                    range_to=ast_node.before_value.as_string().strip("'"),
                    include_upper=False
                )
            raise NotSupportedError("暂不支持的表达式形式（比较运算符前后不是一个字段名、一个字面值）")
        if ast_node.operator.source() == ">=":
            if (isinstance(ast_node.before_value, node.ASTColumnNameExpression)
                    and isinstance(ast_node.after_value, node.ASTLiteralExpression)):
                # 字段名 >= 字面值
                return tablestore.RangeQuery(
                    field_name=ast_node.before_value.column_name,
                    range_from=ast_node.after_value.as_string().strip("'"),
                    include_lower=True
                )
            elif (isinstance(ast_node.before_value, node.ASTLiteralExpression)
                  and isinstance(ast_node.after_value, node.ASTColumnNameExpression)):
                # 字面值 >= 字段名
                return tablestore.RangeQuery(
                    field_name=ast_node.after_value.column_name,
                    range_to=ast_node.before_value.as_string().strip("'"),
                    include_upper=True
                )
            raise NotSupportedError("暂不支持的表达式形式（比较运算符前后不是一个字段名、一个字面值）")
        if ast_node.operator.source() == "!=":
            if (isinstance(ast_node.before_value, node.ASTColumnNameExpression)
                    and isinstance(ast_node.after_value, node.ASTLiteralExpression)):
                # 字段名 != 字面值
                return tablestore.BoolQuery(must_not_queries=[tablestore.TermQuery(
                    field_name=ast_node.before_value.column_name,
                    column_value=ast_node.after_value.as_string().strip("'")
                )])
            elif (isinstance(ast_node.before_value, node.ASTLiteralExpression)
                  and isinstance(ast_node.after_value, node.ASTColumnNameExpression)):
                # 字面值 != 字段名
                return tablestore.BoolQuery(must_not_queries=[tablestore.TermQuery(
                    field_name=ast_node.after_value.column_name,
                    column_value=ast_node.before_value.as_string().strip("'")
                )])
            raise NotSupportedError("暂不支持的表达式形式（比较运算符前后不是一个字段名、一个字面值）")
    if isinstance(ast_node, node.ASTBetweenExpression):  # BETWEEN 表达式
        if not isinstance(ast_node.before_value, node.ASTColumnNameExpression):
            raise NotSupportedError("暂不支持的表达式形式（BETWEEN 之前不是字段名）")
        if (not isinstance(ast_node.from_value, node.ASTLiteralExpression) or
                not isinstance(ast_node.to_value, node.ASTLiteralExpression)):
            raise NotSupportedError("暂不支持的表达式形式（BETWEEN ... AND ... 中的两个值不是字面值）")
        condition = tablestore.RangeQuery(
            field_name=ast_node.before_value.column_name,
            range_from=ast_node.from_value.as_string().strip("'"),
            include_lower=True,
            range_to=ast_node.to_value.as_string().strip("'"),
            include_upper=True
        )
        if ast_node.is_not:
            return tablestore.BoolQuery(must_not_queries=[condition])
        else:
            return condition
    if isinstance(ast_node, node.ASTIsExpression):  # IS NULL 或 IS NOT NULL
        if not isinstance(ast_node.before_value, node.ASTColumnNameExpression):
            raise NotSupportedError("暂不支持的表达式形式（IS 之前不是字段名）")
        if not isinstance(ast_node.after_value, node.ASTLiteralExpression) or ast_node.after_value.value is not None:
            raise NotSupportedError("暂不支持的表达式形式（IS 或 IS NOT 后不是 NULL）")
        condition = tablestore.ExistsQuery(ast_node.before_value.column_name)
        if ast_node.is_not:
            return tablestore.BoolQuery(must_not_queries=[condition])
        else:
            return condition
    if isinstance(ast_node, node.ASTInExpression):  # IN 语句
        if not isinstance(ast_node.before_value, node.ASTColumnNameExpression):
            raise NotSupportedError("暂不支持的表达式形式（IN 之前不是字段名）")
        if not isinstance(ast_node.after_value, node.ASTSubValueExpression):
            raise NotSupportedError("暂不支持的表达式形式（IN 之后不是值列表）")
        condition = tablestore.TermsQuery(ast_node.before_value.column_name,
                                          [value.source().strip("'") for value in ast_node.after_value.values])
        if ast_node.is_not:
            return tablestore.BoolQuery(must_not_queries=[condition])
        else:
            return condition
    if isinstance(ast_node, node.ASTLikeExpression):  # LIKE 语句
        if not isinstance(ast_node.before_value, node.ASTColumnNameExpression):
            raise NotSupportedError("暂不支持的表达式形式（LIKE 之前不是字段名）")
        if not isinstance(ast_node.after_value, node.ASTLiteralExpression):
            raise NotSupportedError("暂不支持的表达式形式（LIKE 之后不是字面值）")
        condition = tablestore.WildcardQuery(ast_node.before_value.column_name,
                                             ast_node.after_value.as_string().strip("'").replace("%", "*"))
        if ast_node.is_not:
            return tablestore.BoolQuery(must_not_queries=[condition])
        else:
            return condition
    if isinstance(ast_node, node.ASTLogicalAndExpression):  # 逻辑与表达式
        condition1 = change_ast_node_to_tablestore_query(ast_node.before_value)
        condition2 = change_ast_node_to_tablestore_query(ast_node.after_value)
        return tablestore.BoolQuery(must_queries=[condition1, condition2])
    if isinstance(ast_node, node.ASTLogicalOrExpression):  # 逻辑或表达式
        condition1 = change_ast_node_to_tablestore_query(ast_node.before_value)
        condition2 = change_ast_node_to_tablestore_query(ast_node.after_value)
        return tablestore.BoolQuery(should_queries=[condition1, condition2])
    if isinstance(ast_node, node.ASTLogicalNotExpression):  # 逻辑否表达式
        condition1 = change_ast_node_to_tablestore_query(ast_node.expression)
        return tablestore.BoolQuery(must_not_queries=[condition1])
    if isinstance(ast_node, node.ASTLogicalXorExpression):  # 逻辑异或表达式
        raise NotSupportedError("无法使用多元索引（不支持逻辑异或的查询方法）")
    raise KeyError(f"暂无法支持的 WHERE 条件（不是比较运算符的形式）: {ast_node}")
