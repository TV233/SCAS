package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.TopText;
import com.kclgroup.backend.service.TopTextService;
import com.kclgroup.backend.mapper.TopTextMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
* @author 张小明
* @description 针对表【top_text】的数据库操作Service实现
* @createDate 2024-06-24 15:22:14
*/
@Service
public class TopTextServiceImpl extends ServiceImpl<TopTextMapper, TopText>
    implements TopTextService{
    @Autowired
    TopTextMapper topTextMapper;

    @Override
    public TopText getTopText() {
        return topTextMapper.getTopText();
    }
}




