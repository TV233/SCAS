package com.kclgroup.backend.mapper;

import com.kclgroup.backend.pojo.entity.StockIndices;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.kclgroup.backend.pojo.vo.StockIndicesVo;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
* @author 张小明
* @description 针对表【stock_indices】的数据库操作Mapper
* @createDate 2024-07-01 21:31:24
* @Entity com.kclgroup.backend.pojo.entity.StockIndices
*/
@Mapper
public interface StockIndicesMapper extends BaseMapper<StockIndices> {
    @Select("select * from stock_indices")
    List<StockIndicesVo> getStockIndices();
}




