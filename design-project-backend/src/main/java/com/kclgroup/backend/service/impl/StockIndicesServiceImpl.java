package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.StockIndices;
import com.kclgroup.backend.pojo.vo.StockIndicesVo;
import com.kclgroup.backend.service.StockIndicesService;
import com.kclgroup.backend.mapper.StockIndicesMapper;
import org.springframework.stereotype.Service;

import java.util.List;

/**
* @author 张小明
* @description 针对表【stock_indices】的数据库操作Service实现
* @createDate 2024-07-01 21:31:24
*/
@Service
public class StockIndicesServiceImpl extends ServiceImpl<StockIndicesMapper, StockIndices>
    implements StockIndicesService{

    @Override
    public List<StockIndicesVo> getStockIndices() {
        List<StockIndicesVo> stockIndices = baseMapper.getStockIndices();
        return stockIndices;
    }
}




