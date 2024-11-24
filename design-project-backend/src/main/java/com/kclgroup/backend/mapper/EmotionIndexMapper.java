package com.kclgroup.backend.mapper;

import com.kclgroup.backend.pojo.entity.EmotionIndex;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

/**
* @author 张小明
* @description 针对表【emotion_index】的数据库操作Mapper
* @createDate 2024-06-24 20:48:29
* @Entity com.kclgroup.backend.pojo.entity.EmotionIndex
*/
@Mapper
public interface EmotionIndexMapper extends BaseMapper<EmotionIndex> {
    @Select("SELECT emotion_index FROM emotion_index LIMIT 1")
    EmotionIndex getEmotionIndex();
}




