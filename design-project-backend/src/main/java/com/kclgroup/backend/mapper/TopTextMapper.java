package com.kclgroup.backend.mapper;

import com.kclgroup.backend.pojo.entity.TopText;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.kclgroup.backend.pojo.entity.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

/**
* @author 张小明
* @description 针对表【top_text】的数据库操作Mapper
* @createDate 2024-06-24 15:22:14
* @Entity com.kclgroup.backend.pojo.entity.TopText
*/
@Mapper
public interface TopTextMapper extends BaseMapper<TopText>{
    @Select("SELECT position_index, title, content FROM top_text LIMIT 1")
    TopText getTopText();
}



