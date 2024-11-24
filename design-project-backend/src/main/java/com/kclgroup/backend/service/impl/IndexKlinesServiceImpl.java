package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.IndexKlines;
import com.kclgroup.backend.pojo.vo.IndexKlineVo;
import com.kclgroup.backend.service.IndexKlinesService;
import com.kclgroup.backend.mapper.IndexKlinesMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
* @author 张小明
* @description 针对表【index_klines】的数据库操作Service实现
* @createDate 2024-07-02 13:08:39
*/
@Service
public class IndexKlinesServiceImpl extends ServiceImpl<IndexKlinesMapper, IndexKlines>
    implements IndexKlinesService{

    @Autowired
    private IndexKlinesMapper indexKlinesMapper;
    @Override
    public List<IndexKlineVo> getIndexKlines(String indexCode) {
        List<IndexKlineVo> indexKlines = indexKlinesMapper.getIndexKlines(indexCode);
        return indexKlines;
    }
}




