package com.kclgroup.backend.mapper;

import com.kclgroup.backend.pojo.entity.FinancialData;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
* @author 张小明
* @description 针对表【financial_data】的数据库操作Mapper
* @createDate 2024-06-25 16:35:57
* @Entity com.kclgroup.backend.pojo.entity.FinancialData
*/
@Mapper
public interface FinancialDataMapper extends BaseMapper<FinancialData> {
    @Select("select * from financial_data where stock_code=#{stockCode}")
    FinancialData getByStockCode(String stockCode);
    @Select("select * from financial_data where stock_code=#{stockCode}")
    List<FinancialData> findByStockCode(String stockCode);
}




