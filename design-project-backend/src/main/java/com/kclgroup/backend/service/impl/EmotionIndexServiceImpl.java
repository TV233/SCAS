package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.EmotionIndex;
import com.kclgroup.backend.service.EmotionIndexService;
import com.kclgroup.backend.mapper.EmotionIndexMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
* @author 张小明
* @description 针对表【emotion_index】的数据库操作Service实现
* @createDate 2024-06-24 20:48:29
*/
@Service
public class EmotionIndexServiceImpl extends ServiceImpl<EmotionIndexMapper, EmotionIndex>
    implements EmotionIndexService{
    @Autowired
    EmotionIndexMapper emotionIndexMapper;
    @Override
    public EmotionIndex getEmotionIndex() {
        return emotionIndexMapper.getEmotionIndex();
    }
}




