package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.SectorsAndStocks;
import com.kclgroup.backend.service.SectorsAndStocksService;
import com.kclgroup.backend.mapper.SectorsAndStocksMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
* @author 张小明
* @description 针对表【sectors_and_stocks】的数据库操作Service实现
* @createDate 2024-06-24 20:57:12
*/
@Service
public class SectorsAndStocksServiceImpl extends ServiceImpl<SectorsAndStocksMapper, SectorsAndStocks>
    implements SectorsAndStocksService{
    @Autowired
    private SectorsAndStocksMapper sectorsAndStocksMapper;
    @Override
    public List<SectorsAndStocks> getSectorsAndStocks() {
        return sectorsAndStocksMapper.getSectorsAndStocks();
    }
}




